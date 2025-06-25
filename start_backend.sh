#!/bin/bash

echo "🚀 백엔드 서버를 시작합니다..."

# 가상환경 활성화
source venv/bin/activate

# 백엔드 서버 시작
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload 