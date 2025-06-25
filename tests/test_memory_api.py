import pytest
import sys
import os
from fastapi.testclient import TestClient

# 백엔드 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.main import app


class TestMemoryAPI:
    """메모리 통합 API 테스트"""
    
    @pytest.fixture
    def client(self):
        """FastAPI 테스트 클라이언트"""
        return TestClient(app)
    
    def test_chat_with_session_id(self, client):
        """세션 ID를 포함한 채팅 API 테스트"""
        chat_data = {
            "message": "안녕하세요",
            "session_id": "test_session_123",
            "user_id": "test_user_456"
        }
        
        response = client.post("/chat/", json=chat_data)
        
        assert response.status_code == 200
        response_data = response.json()
        
        assert "response" in response_data
        assert "session_id" in response_data
        assert "context_used" in response_data
        assert response_data["session_id"] == chat_data["session_id"]
    
    def test_chat_without_session_id(self, client):
        """세션 ID 없는 채팅 API 테스트 (자동 생성)"""
        chat_data = {
            "message": "안녕하세요",
            "user_id": "test_user_456"
        }
        
        response = client.post("/chat/", json=chat_data)
        
        assert response.status_code == 200
        response_data = response.json()
        
        assert "response" in response_data
        assert "session_id" in response_data
        assert response_data["session_id"] is not None
        assert len(response_data["session_id"]) > 0
    
    def test_multiturn_conversation(self, client):
        """멀티턴 대화 테스트"""
        session_id = "test_multiturn_session"
        user_id = "test_user"
        
        # 첫 번째 메시지
        first_message = {
            "message": "안녕하세요, 제 이름은 김철수입니다",
            "session_id": session_id,
            "user_id": user_id
        }
        
        response1 = client.post("/chat/", json=first_message)
        assert response1.status_code == 200
        
        # 두 번째 메시지 (이전 대화 참조)
        second_message = {
            "message": "제 이름이 뭐라고 했죠?",
            "session_id": session_id,
            "user_id": user_id
        }
        
        response2 = client.post("/chat/", json=second_message)
        assert response2.status_code == 200
        
        response2_data = response2.json()
        
        # 컨텍스트가 사용되었는지 확인
        assert response2_data["context_used"] is True
        # 이름이 응답에 포함되었는지 확인 (메모리 활용)
        assert "김철수" in response2_data["response"] or "이름" in response2_data["response"]
    
    def test_session_history_endpoint(self, client):
        """세션 히스토리 조회 API 테스트"""
        session_id = "test_history_session"
        user_id = "test_user"
        
        # 메시지 몇 개 보내기
        messages = ["첫 번째 메시지", "두 번째 메시지", "세 번째 메시지"]
        
        for message in messages:
            chat_data = {
                "message": message,
                "session_id": session_id,
                "user_id": user_id
            }
            client.post("/chat/", json=chat_data)
        
        # 히스토리 조회
        response = client.get(f"/chat/history/{user_id}/{session_id}")
        
        assert response.status_code == 200
        history_data = response.json()
        
        assert "history" in history_data
        assert len(history_data["history"]) >= len(messages)  # user + assistant 메시지
    
    def test_new_session_endpoint(self, client):
        """새 세션 생성 API 테스트"""
        user_id = "test_user"
        
        response = client.post(f"/chat/new-session/{user_id}")
        
        assert response.status_code == 200
        session_data = response.json()
        
        assert "session_id" in session_data
        assert "user_id" in session_data
        assert session_data["user_id"] == user_id
        assert len(session_data["session_id"]) > 0
    
    def test_invalid_request_data(self, client):
        """잘못된 요청 데이터 테스트"""
        # 필수 필드 누락
        invalid_data = {
            "user_id": "test_user"
            # message 필드 누락
        }
        
        response = client.post("/chat/", json=invalid_data)
        
        assert response.status_code == 422  # Validation Error
    
    def test_empty_message(self, client):
        """빈 메시지 테스트"""
        chat_data = {
            "message": "",
            "user_id": "test_user"
        }
        
        response = client.post("/chat/", json=chat_data)
        
        assert response.status_code == 422  # Validation Error 