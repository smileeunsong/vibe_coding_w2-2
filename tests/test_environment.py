import os


def test_env_example_exists():
    """.env.example 파일이 존재하는지 확인"""
    assert os.path.exists(".env.example"), ".env.example 파일이 존재하지 않습니다"


def test_env_example_contains_gemini_key():
    """.env.example에 GEMINI_API_KEY가 포함되어 있는지 확인"""
    with open(".env.example", "r") as f:
        content = f.read()
    assert "GEMINI_API_KEY" in content, ".env.example에 GEMINI_API_KEY가 포함되어 있지 않습니다"


def test_env_example_contains_langsmith_key():
    """.env.example에 LANGSMITH_API_KEY가 포함되어 있는지 확인"""
    with open(".env.example", "r") as f:
        content = f.read()
    assert "LANGSMITH_API_KEY" in content, ".env.example에 LANGSMITH_API_KEY가 포함되어 있지 않습니다" 