from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..models import ChatRequest, ChatResponse, ErrorResponse
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 라우터 생성
router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 요청"},
        500: {"model": ErrorResponse, "description": "서버 에러"}
    }
)


@router.post("/", response_model=ChatResponse, summary="채팅 메시지 전송")
async def chat_endpoint(request: ChatRequest):
    """
    사용자 메시지를 받아 AI 응답을 생성합니다.
    
    - **message**: 사용자의 메시지 (1-1000자)
    """
    try:
        logger.info(f"채팅 요청 수신: {request.message}")
        
        # 현재는 간단한 더미 응답 (나중에 LangGraph 연동 예정)
        response_message = f"안녕하세요! 메시지를 잘 받았습니다: '{request.message}'"
        
        response = ChatResponse(
            response=response_message,
            timestamp=datetime.now()
        )
        
        logger.info(f"채팅 응답 생성 완료")
        return response
        
    except Exception as e:
        logger.error(f"채팅 처리 중 에러 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"채팅 처리 중 에러가 발생했습니다: {str(e)}"
        ) 