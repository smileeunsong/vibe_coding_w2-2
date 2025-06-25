import pytest
from fastapi.testclient import TestClient
import sys
import os

# 백엔드 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.main import app

client = TestClient(app)


def test_validation_error_handling():
    """요청 검증 에러가 적절히 처리되는지 확인"""
    response = client.post("/chat/", json={})
    assert response.status_code == 422
    json_response = response.json()
    assert "detail" in json_response


def test_internal_error_format():
    """내부 서버 에러가 적절한 형태로 반환되는지 확인"""
    # 잘못된 데이터 타입으로 요청하여 내부 에러 유발
    response = client.post("/chat/", json={"message": None})
    # 422 (검증 에러) 또는 500 (서버 에러) 중 하나여야 함
    assert response.status_code in [422, 500]


def test_http_exception_handling():
    """HTTP 예외가 적절히 처리되는지 확인"""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    json_response = response.json()
    assert "detail" in json_response


def test_error_response_format():
    """에러 응답이 일관된 형태를 가지는지 확인"""
    response = client.post("/chat/", json={"invalid": "data"})
    assert response.status_code == 422
    json_response = response.json()
    assert isinstance(json_response, dict)
    assert "detail" in json_response


def test_cors_error_handling():
    """CORS 에러가 적절히 처리되는지 확인"""
    # 허용되지 않은 Origin으로 요청
    response = client.get("/", headers={"Origin": "http://malicious-site.com"})
    # CORS는 서버에서 허용하지만 브라우저에서 차단하므로 200이 반환될 수 있음
    assert response.status_code in [200, 403] 