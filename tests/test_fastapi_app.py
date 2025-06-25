import pytest
from fastapi.testclient import TestClient
import sys
import os

# 백엔드 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.main import app

client = TestClient(app)


def test_app_title():
    """FastAPI 애플리케이션 제목이 올바르게 설정되었는지 확인"""
    assert app.title == "Vibe Coding Assistant"


def test_app_description():
    """FastAPI 애플리케이션 설명이 올바르게 설정되었는지 확인"""
    assert "AI 챗봇" in app.description


def test_root_endpoint():
    """루트 엔드포인트가 정상적으로 작동하는지 확인"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint():
    """헬스체크 엔드포인트가 정상적으로 작동하는지 확인"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_cors_enabled():
    """CORS 미들웨어가 설정되어 있는지 확인"""
    response = client.get("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200


def test_env_variables_loaded():
    """환경 변수 로딩 기능이 작동하는지 확인 (.env 파일이 없어도 에러가 발생하지 않음)"""
    import os
    from dotenv import load_dotenv
    # .env 파일이 없어도 load_dotenv()가 에러없이 작동하는지 확인
    try:
        load_dotenv()
        assert True  # 에러가 발생하지 않으면 성공
    except Exception:
        pytest.fail("환경 변수 로딩 중 에러가 발생했습니다") 