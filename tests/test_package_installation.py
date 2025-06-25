import pytest


def test_fastapi_import():
    """FastAPI가 정상적으로 import되는지 확인"""
    try:
        import fastapi
        assert True
    except ImportError:
        pytest.fail("FastAPI를 import할 수 없습니다")


def test_streamlit_import():
    """Streamlit이 정상적으로 import되는지 확인"""
    try:
        import streamlit
        assert True
    except ImportError:
        pytest.fail("Streamlit을 import할 수 없습니다")


def test_main_app_import():
    """백엔드 main 모듈을 import할 수 있는지 확인"""
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.getcwd(), "backend"))
        from app.main import app
        assert app is not None
    except ImportError:
        pytest.fail("백엔드 main 모듈을 import할 수 없습니다") 