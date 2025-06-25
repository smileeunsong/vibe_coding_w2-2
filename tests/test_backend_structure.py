import os
import pytest


def test_backend_directory_exists():
    """백엔드 디렉토리가 존재하는지 확인"""
    assert os.path.exists("backend"), "backend 디렉토리가 존재하지 않습니다"


def test_backend_app_directory_exists():
    """백엔드 app 디렉토리가 존재하는지 확인"""
    assert os.path.exists("backend/app"), "backend/app 디렉토리가 존재하지 않습니다"


def test_backend_routers_directory_exists():
    """백엔드 routers 디렉토리가 존재하는지 확인"""
    assert os.path.exists("backend/app/routers"), "backend/app/routers 디렉토리가 존재하지 않습니다"


def test_main_py_exists():
    """main.py 파일이 존재하는지 확인"""
    assert os.path.exists("backend/app/main.py"), "backend/app/main.py 파일이 존재하지 않습니다"


def test_routers_init_exists():
    """routers __init__.py 파일이 존재하는지 확인"""
    assert os.path.exists("backend/app/routers/__init__.py"), "backend/app/routers/__init__.py 파일이 존재하지 않습니다" 