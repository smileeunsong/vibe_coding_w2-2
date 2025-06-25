#!/bin/bash

echo "🎨 프론트엔드 애플리케이션을 시작합니다..."

# 가상환경 활성화
source venv/bin/activate

# 프론트엔드 애플리케이션 시작
streamlit run frontend/app.py --server.port 8501 