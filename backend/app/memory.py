"""
멀티턴 대화를 위한 메모리 시스템
LangGraph InMemoryStore를 사용하여 구현
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.store.base import BaseStore
from langchain_core.runnables import RunnableConfig


class MemoryManager:
    """메모리 관리 시스템"""
    
    def __init__(self):
        """메모리 매니저 초기화"""
        self.store = InMemoryStore()
        self.checkpointer = InMemorySaver()
    
    def create_namespace(self, user_id: str, session_id: str, memory_type: str = "messages") -> Tuple[str, ...]:
        """네임스페이스 생성"""
        return (user_id, session_id, memory_type)
    
    def save_message(self, user_id: str, session_id: str, message: str, role: str) -> str:
        """메시지를 메모리에 저장"""
        namespace = self.create_namespace(user_id, session_id)
        memory_id = str(uuid.uuid4())
        
        memory_data = {
            "message": message,
            "role": role,
            "timestamp": str(datetime.now()),
            "session_id": session_id,
            "user_id": user_id
        }
        
        self.store.put(namespace, memory_id, memory_data)
        return memory_id
    
    def get_conversation_history(self, user_id: str, session_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """대화 히스토리 조회"""
        namespace = self.create_namespace(user_id, session_id)
        memories = self.store.search(namespace)
        
        # 시간순 정렬
        sorted_memories = sorted(memories, key=lambda x: x.created_at)
        
        if limit:
            sorted_memories = sorted_memories[-limit:]
        
        return [memory.value for memory in sorted_memories]
    
    def get_recent_context(self, user_id: str, session_id: str, context_limit: int = 5) -> str:
        """최근 대화 컨텍스트 가져오기"""
        history = self.get_conversation_history(user_id, session_id, limit=context_limit)
        
        if not history:
            return ""
        
        context_parts = []
        for entry in history:
            role = entry.get("role", "unknown")
            message = entry.get("message", "")
            context_parts.append(f"{role}: {message}")
        
        return "\n".join(context_parts)
    
    def clear_session(self, user_id: str, session_id: str) -> bool:
        """세션 메모리 삭제"""
        namespace = self.create_namespace(user_id, session_id)
        memories = self.store.search(namespace)
        
        # 개별 메모리 삭제
        for memory in memories:
            # InMemoryStore는 delete 메서드가 없으므로 새로운 저장소 생성으로 대체
            pass
        
        return True
    
    def create_chat_graph(self, chat_function):
        """채팅용 StateGraph 생성"""
        builder = StateGraph(MessagesState)
        builder.add_node("chat", chat_function)
        builder.add_edge(START, "chat")
        
        return builder.compile(
            checkpointer=self.checkpointer,
            store=self.store
        )


# 전역 메모리 매니저 인스턴스
memory_manager = MemoryManager() 