import os


def test_requirements_txt_exists():
    """requirements.txt 파일이 존재하는지 확인"""
    assert os.path.exists("backend/requirements.txt"), "backend/requirements.txt 파일이 존재하지 않습니다"


def test_requirements_txt_contains_fastapi():
    """requirements.txt에 FastAPI가 포함되어 있는지 확인"""
    with open("backend/requirements.txt", "r") as f:
        content = f.read()
    assert "fastapi" in content.lower(), "requirements.txt에 fastapi가 포함되어 있지 않습니다"


def test_requirements_txt_contains_uvicorn():
    """requirements.txt에 uvicorn이 포함되어 있는지 확인"""
    with open("backend/requirements.txt", "r") as f:
        content = f.read()
    assert "uvicorn" in content.lower(), "requirements.txt에 uvicorn이 포함되어 있지 않습니다"


def test_requirements_txt_contains_langgraph():
    """requirements.txt에 langgraph가 포함되어 있는지 확인"""
    with open("backend/requirements.txt", "r") as f:
        content = f.read()
    assert "langgraph" in content.lower(), "requirements.txt에 langgraph가 포함되어 있지 않습니다" 