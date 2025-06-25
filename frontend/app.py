import streamlit as st
import requests
import uuid
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="Vibe Coding Assistant",
    page_icon="🤖",
    layout="wide"
)

# 세션 상태 초기화
def initialize_session_state():
    """세션 상태 초기화"""
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"user_{str(uuid.uuid4())[:8]}"
    
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

# API 호출 함수
def call_chat_api(message, backend_url, user_id, session_id):
    """채팅 API 호출"""
    try:
        response = requests.post(
            f"{backend_url}/chat/",
            json={
                "message": message,
                "user_id": user_id,
                "session_id": session_id
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API 호출 실패: {response.status_code}")
            return None
    
    except requests.exceptions.ConnectionError:
        st.error("백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.")
        return None
    except requests.exceptions.Timeout:
        st.error("요청 시간이 초과되었습니다.")
        return None
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
        return None

def create_new_session(backend_url, user_id):
    """새 세션 생성"""
    try:
        response = requests.post(f"{backend_url}/chat/new-session/{user_id}")
        if response.status_code == 200:
            return response.json()["session_id"]
        else:
            st.error("새 세션 생성에 실패했습니다.")
            return str(uuid.uuid4())
    except:
        st.error("새 세션 생성 중 오류가 발생했습니다.")
        return str(uuid.uuid4())

def load_conversation_history(backend_url, user_id, session_id):
    """대화 히스토리 로드"""
    try:
        response = requests.get(f"{backend_url}/chat/history/{user_id}/{session_id}")
        if response.status_code == 200:
            return response.json()["history"]
        else:
            return []
    except:
        return []

# 세션 상태 초기화
initialize_session_state()

# 제목
st.title("🤖 Vibe Coding Assistant")
st.markdown("AI 챗봇과 멀티턴 대화를 나누세요! 이전 대화를 기억합니다.")

# 사이드바
with st.sidebar:
    st.header("⚙️ 설정")
    backend_url = st.text_input("백엔드 URL", value="http://localhost:8000")
    
    st.divider()
    
    st.header("📋 세션 정보")
    st.text(f"사용자 ID: {st.session_state.user_id}")
    st.text(f"세션 ID: {st.session_state.session_id[:8]}...")
    
    st.divider()
    
    st.header("🔄 세션 관리")
    
    # 새 대화 시작 버튼
    if st.button("🆕 새 대화 시작", use_container_width=True):
        new_session_id = create_new_session(backend_url, st.session_state.user_id)
        st.session_state.session_id = new_session_id
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.rerun()
    
    # 대화 히스토리 로드 버튼
    if st.button("📚 이전 대화 불러오기", use_container_width=True):
        history = load_conversation_history(
            backend_url, 
            st.session_state.user_id, 
            st.session_state.session_id
        )
        if history:
            st.session_state.conversation_history = history
            # Streamlit 메시지 형식으로 변환
            st.session_state.messages = []
            for msg in history:
                st.session_state.messages.append({
                    "role": msg["role"],
                    "content": msg["message"]
                })
            st.success(f"{len(history)}개의 메시지를 불러왔습니다.")
            st.rerun()
        else:
            st.info("불러올 대화 히스토리가 없습니다.")
    
    st.divider()
    
    # 메모리 상태 표시
    st.header("🧠 메모리 상태")
    st.text(f"총 메시지: {len(st.session_state.messages)}")
    if st.session_state.conversation_history:
        st.text(f"히스토리: {len(st.session_state.conversation_history)}개")

# 메인 채팅 영역
st.header("💬 대화")

# 이전 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 채팅 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답
    with st.chat_message("assistant"):
        with st.spinner("AI가 응답을 생성중입니다..."):
            # API 호출
            api_response = call_chat_api(
                prompt, 
                backend_url, 
                st.session_state.user_id, 
                st.session_state.session_id
            )
            
            if api_response:
                response_text = api_response["response"]
                context_used = api_response.get("context_used", False)
                
                # 응답 표시
                st.markdown(response_text)
                
                # 컨텍스트 사용 여부 표시
                if context_used:
                    st.caption("💭 이전 대화 컨텍스트를 활용했습니다.")
                
                # 메시지 저장
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
                # 세션 ID 업데이트 (새로 생성된 경우)
                if "session_id" in api_response:
                    st.session_state.session_id = api_response["session_id"]
            
            else:
                # 백엔드 연결 실패 시 더미 응답
                response_text = "죄송합니다. 현재 백엔드 서버에 연결할 수 없습니다. 서버를 실행해주세요."
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

# 하단 정보
st.markdown("---")
st.caption(f"🔹 세션: {st.session_state.session_id[:8]}... | 💬 메시지: {len(st.session_state.messages)}개") 