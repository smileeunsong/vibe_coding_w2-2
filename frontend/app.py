import streamlit as st
import requests

# 페이지 설정
st.set_page_config(
    page_title="Vibe Coding Assistant",
    page_icon="🤖",
    layout="wide"
)

# 제목
st.title("🤖 Vibe Coding Assistant")
st.markdown("AI 챗봇과 대화를 나누세요!")

# 사이드바
with st.sidebar:
    st.header("설정")
    backend_url = st.text_input("백엔드 URL", value="http://localhost:8000")

# 메인 채팅 영역
if "messages" not in st.session_state:
    st.session_state.messages = []

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

    # AI 응답 (현재는 더미 응답)
    with st.chat_message("assistant"):
        response = "안녕하세요! 현재 백엔드와 연결되지 않은 상태입니다."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response}) 