import pytest
import uuid
import sys
import os
from unittest.mock import Mock, patch

# 백엔드 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.memory import MemoryManager


class TestMultiturnChat:
    """멀티턴 대화 테스트"""
    
    @pytest.fixture
    def memory_manager(self):
        """메모리 매니저 인스턴스 생성"""
        return MemoryManager()
    
    def test_save_and_retrieve_conversation(self, memory_manager):
        """대화 저장 및 검색 테스트"""
        user_id = "test_user"
        session_id = str(uuid.uuid4())
        
        # 대화 시뮬레이션
        messages = [
            ("안녕하세요", "user"),
            ("안녕하세요! 무엇을 도와드릴까요?", "assistant"),
            ("오늘 날씨가 어때요?", "user"),
            ("죄송하지만 실시간 날씨 정보는 확인할 수 없습니다.", "assistant")
        ]
        
        # 메시지 저장
        saved_ids = []
        for message, role in messages:
            message_id = memory_manager.save_message(user_id, session_id, message, role)
            saved_ids.append(message_id)
            assert isinstance(message_id, str)
        
        # 대화 히스토리 검색
        history = memory_manager.get_conversation_history(user_id, session_id)
        
        assert len(history) == 4
        assert history[0]["message"] == "안녕하세요"
        assert history[0]["role"] == "user"
        assert history[-1]["message"] == "죄송하지만 실시간 날씨 정보는 확인할 수 없습니다."
        assert history[-1]["role"] == "assistant"
    
    def test_session_isolation(self, memory_manager):
        """세션별 대화 격리 테스트"""
        user_id = "test_user"
        session1_id = str(uuid.uuid4())
        session2_id = str(uuid.uuid4())
        
        # 세션 1에 메시지 저장
        memory_manager.save_message(user_id, session1_id, "세션1 메시지", "user")
        
        # 세션 2에 메시지 저장
        memory_manager.save_message(user_id, session2_id, "세션2 메시지", "user")
        
        # 각 세션별 히스토리 확인
        session1_history = memory_manager.get_conversation_history(user_id, session1_id)
        session2_history = memory_manager.get_conversation_history(user_id, session2_id)
        
        assert len(session1_history) == 1
        assert len(session2_history) == 1
        assert session1_history[0]["message"] == "세션1 메시지"
        assert session2_history[0]["message"] == "세션2 메시지"
    
    def test_recent_context_generation(self, memory_manager):
        """최근 컨텍스트 생성 테스트"""
        user_id = "test_user"
        session_id = str(uuid.uuid4())
        
        # 여러 메시지 저장
        messages = [
            ("첫 번째 메시지", "user"),
            ("첫 번째 응답", "assistant"),
            ("두 번째 메시지", "user"),
            ("두 번째 응답", "assistant"),
            ("세 번째 메시지", "user"),
            ("세 번째 응답", "assistant")
        ]
        
        for message, role in messages:
            memory_manager.save_message(user_id, session_id, message, role)
        
        # 최근 3개 메시지의 컨텍스트 생성
        context = memory_manager.get_recent_context(user_id, session_id, context_limit=3)
        
        assert "세 번째 응답" in context
        assert "assistant: 세 번째 응답" in context
        assert "user: 세 번째 메시지" in context
        
        # 컨텍스트에 이전 메시지들이 포함되지 않았는지 확인
        assert "첫 번째 메시지" not in context
    
    def test_empty_session_context(self, memory_manager):
        """빈 세션 컨텍스트 테스트"""
        user_id = "test_user"
        session_id = str(uuid.uuid4())
        
        # 빈 세션의 컨텍스트 요청
        context = memory_manager.get_recent_context(user_id, session_id)
        history = memory_manager.get_conversation_history(user_id, session_id)
        
        assert context == ""
        assert len(history) == 0
    
    def test_conversation_limit(self, memory_manager):
        """대화 개수 제한 테스트"""
        user_id = "test_user"
        session_id = str(uuid.uuid4())
        
        # 10개 메시지 저장
        for i in range(10):
            memory_manager.save_message(user_id, session_id, f"메시지 {i}", "user")
        
        # 최근 5개만 조회
        recent_history = memory_manager.get_conversation_history(user_id, session_id, limit=5)
        
        assert len(recent_history) == 5
        assert recent_history[0]["message"] == "메시지 5"
        assert recent_history[-1]["message"] == "메시지 9"
    
    def test_namespace_creation(self, memory_manager):
        """네임스페이스 생성 테스트"""
        user_id = "user123"
        session_id = "session456"
        
        namespace = memory_manager.create_namespace(user_id, session_id)
        
        assert namespace == ("user123", "session456", "messages")
        
        # 다른 메모리 타입 테스트
        custom_namespace = memory_manager.create_namespace(user_id, session_id, "preferences")
        assert custom_namespace == ("user123", "session456", "preferences") 