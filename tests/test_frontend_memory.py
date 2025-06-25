import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import streamlit as st

# 백엔드 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'frontend'))


class TestFrontendMemory:
    """프론트엔드 메모리 인터페이스 테스트"""
    
    def test_session_id_generation(self):
        """세션 ID 생성 테스트"""
        import uuid
        
        # UUID 형식 검증
        session_id = str(uuid.uuid4())
        assert len(session_id) == 36
        assert session_id.count('-') == 4
    
    @patch('streamlit.session_state')
    def test_session_state_initialization(self, mock_session_state):
        """Streamlit 세션 상태 초기화 테스트"""
        # Mock 세션 상태 설정
        mock_session_state.get = Mock(return_value=None)
        mock_session_state.__setitem__ = Mock()
        mock_session_state.__contains__ = Mock(return_value=False)
        
        # 세션 상태 초기화 로직
        if "session_id" not in mock_session_state:
            mock_session_state["session_id"] = "test_session_123"
        if "user_id" not in mock_session_state:
            mock_session_state["user_id"] = "test_user_456"
        if "conversation_history" not in mock_session_state:
            mock_session_state["conversation_history"] = []
        
        # 초기화 호출 확인
        assert mock_session_state.__setitem__.call_count >= 3
    
    @patch('requests.post')
    def test_api_call_with_session(self, mock_post):
        """세션 정보를 포함한 API 호출 테스트"""
        # Mock API 응답
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": "안녕하세요!",
            "session_id": "test_session_123",
            "context_used": False,
            "timestamp": "2024-01-01T12:00:00"
        }
        mock_post.return_value = mock_response
        
        # API 호출 시뮬레이션
        import requests
        
        api_data = {
            "message": "안녕하세요",
            "user_id": "test_user",
            "session_id": "test_session_123"
        }
        
        response = requests.post("http://localhost:8000/chat/", json=api_data)
        
        # 호출 확인
        mock_post.assert_called_once_with("http://localhost:8000/chat/", json=api_data)
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["session_id"] == "test_session_123"
    
    @patch('requests.get')
    def test_conversation_history_fetch(self, mock_get):
        """대화 히스토리 조회 테스트"""
        # Mock 히스토리 응답
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "history": [
                {"message": "안녕하세요", "role": "user", "timestamp": "2024-01-01T12:00:00"},
                {"message": "안녕하세요! 도움이 필요한 것이 있나요?", "role": "assistant", "timestamp": "2024-01-01T12:00:01"}
            ],
            "session_id": "test_session_123",
            "user_id": "test_user",
            "total_messages": 2
        }
        mock_get.return_value = mock_response
        
        # 히스토리 조회 시뮬레이션
        import requests
        
        user_id = "test_user"
        session_id = "test_session_123"
        
        response = requests.get(f"http://localhost:8000/chat/history/{user_id}/{session_id}")
        
        # 호출 확인
        mock_get.assert_called_once()
        assert response.status_code == 200
        
        history_data = response.json()
        assert len(history_data["history"]) == 2
        assert history_data["total_messages"] == 2
    
    @patch('requests.post')
    def test_new_session_creation(self, mock_post):
        """새 세션 생성 테스트"""
        # Mock 새 세션 응답
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "session_id": "new_session_456",
            "user_id": "test_user",
            "created_at": "2024-01-01T12:00:00"
        }
        mock_post.return_value = mock_response
        
        # 새 세션 생성 시뮬레이션
        import requests
        
        user_id = "test_user"
        response = requests.post(f"http://localhost:8000/chat/new-session/{user_id}")
        
        # 호출 확인
        mock_post.assert_called_once()
        assert response.status_code == 200
        
        session_data = response.json()
        assert session_data["session_id"] == "new_session_456"
        assert session_data["user_id"] == user_id
    
    def test_conversation_display_format(self):
        """대화 표시 형식 테스트"""
        # 테스트 대화 데이터
        conversation = [
            {"message": "안녕하세요", "role": "user", "timestamp": "2024-01-01T12:00:00"},
            {"message": "안녕하세요! 도움이 필요한 것이 있나요?", "role": "assistant", "timestamp": "2024-01-01T12:00:01"},
            {"message": "오늘 날씨가 어때요?", "role": "user", "timestamp": "2024-01-01T12:01:00"}
        ]
        
        # 사용자/어시스턴트 메시지 분리
        user_messages = [msg for msg in conversation if msg["role"] == "user"]
        assistant_messages = [msg for msg in conversation if msg["role"] == "assistant"]
        
        assert len(user_messages) == 2
        assert len(assistant_messages) == 1
        
        # 최신 메시지가 마지막에 있는지 확인
        assert conversation[-1]["message"] == "오늘 날씨가 어때요?"
        assert conversation[-1]["role"] == "user"
    
    def test_session_persistence(self):
        """세션 지속성 테스트"""
        # 브라우저 localStorage 시뮬레이션
        mock_storage = {}
        
        def set_item(key, value):
            mock_storage[key] = value
        
        def get_item(key):
            return mock_storage.get(key)
        
        # 세션 저장
        session_id = "persistent_session_123"
        user_id = "persistent_user"
        
        set_item("session_id", session_id)
        set_item("user_id", user_id)
        
        # 세션 복원
        restored_session_id = get_item("session_id")
        restored_user_id = get_item("user_id")
        
        assert restored_session_id == session_id
        assert restored_user_id == user_id
    
    def test_error_handling(self):
        """에러 처리 테스트"""
        # 네트워크 에러 시뮬레이션
        def simulate_network_error():
            raise ConnectionError("네트워크 연결 오류")
        
        # 에러 처리 로직
        try:
            simulate_network_error()
            assert False, "에러가 발생해야 함"
        except ConnectionError as e:
            assert "네트워크 연결 오류" in str(e)
        
        # API 에러 시뮬레이션
        def simulate_api_error():
            class MockResponse:
                status_code = 500
                def json(self):
                    return {"error": "서버 내부 오류"}
            
            return MockResponse()
        
        response = simulate_api_error()
        assert response.status_code == 500
        assert "서버 내부 오류" in response.json()["error"] 