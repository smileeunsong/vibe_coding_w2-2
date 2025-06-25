import pytest
import uuid
from datetime import datetime
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, MessagesState, START


class TestMemorySystem:
    """메모리 시스템 테스트"""
    
    @pytest.fixture
    def memory_store(self):
        """InMemoryStore 인스턴스 생성"""
        return InMemoryStore()
    
    @pytest.fixture
    def checkpointer(self):
        """InMemorySaver 체크포인터 생성"""
        return InMemorySaver()
    
    def test_memory_store_creation(self, memory_store):
        """메모리 저장소 생성 테스트"""
        assert memory_store is not None
        assert isinstance(memory_store, InMemoryStore)
    
    def test_memory_store_put_and_get(self, memory_store):
        """메모리 저장 및 검색 테스트"""
        user_id = "test_user"
        session_id = "test_session"
        namespace = (user_id, session_id, "messages")
        
        memory_id = str(uuid.uuid4())
        memory_data = {
            "message": "안녕하세요",
            "timestamp": str(datetime.now()),
            "role": "user"
        }
        
        # 메모리 저장
        memory_store.put(namespace, memory_id, memory_data)
        
        # 메모리 검색
        retrieved_memory = memory_store.get(namespace, memory_id)
        
        assert retrieved_memory is not None
        assert retrieved_memory.value == memory_data
        assert retrieved_memory.key == memory_id
        assert retrieved_memory.namespace == namespace
    
    def test_memory_search(self, memory_store):
        """메모리 검색 테스트"""
        user_id = "test_user"
        session_id = "test_session"
        namespace = (user_id, session_id, "messages")
        
        # 여러 메모리 저장
        memories = [
            {"message": "안녕하세요", "role": "user"},
            {"message": "반갑습니다", "role": "assistant"},
            {"message": "오늘 날씨가 좋네요", "role": "user"}
        ]
        
        for i, memory in enumerate(memories):
            memory_store.put(namespace, f"mem_{i}", memory)
        
        # 모든 메모리 검색
        all_memories = memory_store.search(namespace)
        
        assert len(all_memories) == 3
        assert all([mem.namespace == namespace for mem in all_memories])
    
    def test_user_namespace_isolation(self, memory_store):
        """사용자별 메모리 네임스페이스 격리 테스트"""
        user1_namespace = ("user1", "session1", "messages")
        user2_namespace = ("user2", "session1", "messages")
        
        # 각 사용자별로 메모리 저장
        memory_store.put(user1_namespace, "mem1", {"message": "User1 message"})
        memory_store.put(user2_namespace, "mem2", {"message": "User2 message"})
        
        # 각 사용자 메모리 검색
        user1_memories = memory_store.search(user1_namespace)
        user2_memories = memory_store.search(user2_namespace)
        
        assert len(user1_memories) == 1
        assert len(user2_memories) == 1
        assert user1_memories[0].value["message"] == "User1 message"
        assert user2_memories[0].value["message"] == "User2 message"
    
    def test_checkpointer_creation(self, checkpointer):
        """체크포인터 생성 테스트"""
        assert checkpointer is not None
        assert isinstance(checkpointer, InMemorySaver)
    
    def test_state_graph_creation(self, memory_store, checkpointer):
        """StateGraph 생성 및 컴파일 테스트"""
        def dummy_node(state: MessagesState):
            return {"messages": []}
        
        builder = StateGraph(MessagesState)
        builder.add_node("dummy", dummy_node)
        builder.add_edge(START, "dummy")
        
        # 메모리 저장소와 체크포인터로 그래프 컴파일
        graph = builder.compile(
            checkpointer=checkpointer,
            store=memory_store
        )
        
        assert graph is not None 