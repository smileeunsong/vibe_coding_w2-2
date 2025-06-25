# Vibe Coding Assistant

AI 챗봇 애플리케이션입니다.

## 프로젝트 구조

```
vibe_coding_w2-1/
├── backend/              # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py       # FastAPI 애플리케이션
│   │   └── routers/      # API 라우터
│   └── requirements.txt  # 백엔드 의존성
├── frontend/             # Streamlit 프론트엔드
│   ├── app.py           # Streamlit 애플리케이션
│   └── requirements.txt # 프론트엔드 의존성
├── tests/               # 테스트 코드
└── .env.example         # 환경 변수 예시
```

## 빠른 시작

### 1. 환경 설정

```bash
# 가상환경 활성화
source venv/bin/activate

# 백엔드 패키지 설치
pip install -r backend/requirements.txt

# 프론트엔드 패키지 설치
pip install -r frontend/requirements.txt
```

### 2. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일을 편집하여 API 키 설정
# GEMINI_API_KEY=your_api_key_here
```

### 3. 애플리케이션 실행

#### 백엔드 서버 시작

```bash
./start_backend.sh
```

백엔드 서버: http://localhost:8000

#### 프론트엔드 애플리케이션 시작

```bash
./start_frontend.sh
```

프론트엔드 애플리케이션: http://localhost:8501

### 4. 테스트 실행

```bash
# 전체 테스트 실행
python -m pytest tests/ -v

# 특정 테스트 실행
python -m pytest tests/test_backend_structure.py -v
```

## API 엔드포인트

- `GET /` - 기본 정보
- `GET /health` - 헬스체크

## 기술 스택

### 백엔드

- FastAPI
- LangGraph
- Gemini LLM
- DuckDuckGo Search

### 프론트엔드

- Streamlit
- Streamlit Chat

### 개발 도구

- pytest (테스팅)
- uvicorn (ASGI 서버)
