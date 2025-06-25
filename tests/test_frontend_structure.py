import os


def test_frontend_directory_exists():
    """프론트엔드 디렉토리가 존재하는지 확인"""
    assert os.path.exists("frontend"), "frontend 디렉토리가 존재하지 않습니다"


def test_frontend_requirements_exists():
    """프론트엔드 requirements.txt가 존재하는지 확인"""
    assert os.path.exists("frontend/requirements.txt"), "frontend/requirements.txt 파일이 존재하지 않습니다"


def test_frontend_app_py_exists():
    """프론트엔드 app.py가 존재하는지 확인"""
    assert os.path.exists("frontend/app.py"), "frontend/app.py 파일이 존재하지 않습니다"


def test_frontend_requirements_contains_streamlit():
    """frontend requirements.txt에 streamlit이 포함되어 있는지 확인"""
    with open("frontend/requirements.txt", "r") as f:
        content = f.read()
    assert "streamlit" in content.lower(), "frontend/requirements.txt에 streamlit이 포함되어 있지 않습니다" 