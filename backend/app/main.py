from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# 라우터 import
from .routers import chat
from .models import ErrorResponse

# 환경 변수 로드
load_dotenv()

# FastAPI 애플리케이션 초기화
app = FastAPI(
    title="Vibe Coding Assistant",
    description="AI 챗봇 애플리케이션 백엔드",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000"],  # Streamlit과 React 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 에러 핸들러 등록
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """요청 검증 에러 핸들러"""
    logging.error(f"요청 검증 에러: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "요청 데이터 검증 실패",
            "detail": exc.errors(),
            "timestamp": str(datetime.now())
        }
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """HTTP 예외 핸들러"""
    logging.error(f"HTTP 에러: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": f"HTTP {exc.status_code} 에러",
            "detail": exc.detail,
            "timestamp": str(datetime.now())
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """일반 예외 핸들러"""
    logging.error(f"예상치 못한 에러: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "내부 서버 에러",
            "detail": "서버에서 예상치 못한 에러가 발생했습니다.",
            "timestamp": str(datetime.now())
        }
    )


# 라우터 등록
app.include_router(chat.router)


@app.get("/", tags=["Root"])
async def read_root():
    """루트 엔드포인트"""
    return {"message": "Vibe Coding Assistant API"}


@app.get("/health", tags=["Health"])
async def health_check():
    """서버 헬스체크 엔드포인트입니다."""
    return {
        status: "healthy",  # 의도적 버그: "status" 키에 따옴표 누락
        "message": "서버가 정상적으로 실행중입니다."
    }


@app.get("/test")
async def test_endpoint():
    """테스트용 엔드포인트입니다. GitHub Actions 자동화 테스트를 위해 추가되었습니다."""
    return {
        "message": "테스트 엔드포인트가 성공적으로 호출되었습니다! 🚀",
        "test_data": {
            "timestamp": "2024-06-25",
            "purpose": "GitHub Actions 자동화 테스트",
            "features": [
                "자동 PR 생성",
                "자동 리뷰어 할당", 
                "자동 라벨링",
                "코드 품질 검사",
                "테스트 실행"
            ]
        },
        "success": True
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True
    ) 