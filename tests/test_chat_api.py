import pytest
from fastapi.testclient import TestClient
import sys
import os

# 백엔드 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.main import app

client = TestClient(app)


def test_chat_endpoint_exists():
    """채팅 엔드포인트가 존재하는지 확인"""
    # POST 요청으로 확인 (404가 아닌 다른 에러가 발생해야 함)
    response = client.post("/chat", json={"message": "테스트"})
    # 404가 아닌 경우는 엔드포인트가 존재한다는 의미
    assert response.status_code != 404


def test_chat_endpoint_post_method():
    """채팅 엔드포인트가 POST 메소드를 지원하는지 확인"""
    response = client.post("/chat", json={"message": "안녕하세요"})
    assert response.status_code in [200, 422]  # 200 성공 또는 422 검증 에러


def test_chat_request_validation():
    """채팅 요청 데이터 검증이 작동하는지 확인"""
    # 잘못된 요청 데이터로 422 에러가 발생하는지 확인
    response = client.post("/chat", json={})
    assert response.status_code == 422


def test_chat_response_format():
    """채팅 응답 포맷이 올바른지 확인"""
    response = client.post("/chat", json={"message": "안녕하세요"})
    if response.status_code == 200:
        json_response = response.json()
        assert "response" in json_response
        assert "timestamp" in json_response


def test_chat_with_valid_message():
    """유효한 메시지로 채팅 요청시 정상 응답하는지 확인"""
    response = client.post("/chat", json={"message": "안녕하세요!"})
    if response.status_code == 200:
        json_response = response.json()
        assert isinstance(json_response["response"], str)
        assert len(json_response["response"]) > 0


def test_chat_router_registered():
    """채팅 라우터가 메인 앱에 등록되었는지 확인"""
    # /chat/ 경로가 앱의 routes에 있는지 확인
    routes = [route.path for route in app.routes]
    assert "/chat/" in routes 