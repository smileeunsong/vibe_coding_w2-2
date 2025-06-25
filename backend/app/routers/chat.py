from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..models import ChatRequest, ChatResponse, ErrorResponse, SessionResponse, ConversationHistory
from ..memory import memory_manager
from datetime import datetime
import logging
import uuid

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


@router.post("/", response_model=ChatResponse, summary="멀티턴 채팅 메시지 전송")
async def chat_endpoint(request: ChatRequest):
    """
    사용자 메시지를 받아 AI 응답을 생성합니다. 이전 대화 컨텍스트를 활용합니다.
    
    - **message**: 사용자의 메시지 (1-1000자)
    - **user_id**: 사용자 ID
    - **session_id**: 세션 ID (선택사항, 없으면 자동 생성)
    """
    try:
        # 빈 메시지 검증
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="메시지가 비어있습니다.")
        
        logger.info(f"채팅 요청 수신 - User: {request.user_id}, Message: {request.message}")
        
        # 세션 ID 생성 또는 사용
        session_id = request.session_id or str(uuid.uuid4())
        
        # 사용자 메시지 저장
        memory_manager.save_message(request.user_id, session_id, request.message, "user")
        
        # 이전 대화 컨텍스트 가져오기
        context = memory_manager.get_recent_context(request.user_id, session_id, context_limit=5)
        context_used = len(context) > 0
        
        # AI 응답 생성 (현재는 더미 응답, 향후 LangGraph 연동)
        if context_used:
            response_message = f"이전 대화를 기억하고 있습니다. 현재 메시지: '{request.message}'"
            if "이름" in request.message and "김철수" in context:
                response_message = "김철수님, 안녕하세요! 기억하고 있습니다."
        else:
            response_message = f"안녕하세요! 메시지를 잘 받았습니다: '{request.message}'"
        
        # AI 응답 저장
        memory_manager.save_message(request.user_id, session_id, response_message, "assistant")
        
        response = ChatResponse(
            response=response_message,
            session_id=session_id,
            context_used=context_used,
            timestamp=datetime.now()
        )
        
        logger.info(f"채팅 응답 생성 완료 - Session: {session_id}, Context Used: {context_used}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"채팅 처리 중 에러 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"채팅 처리 중 에러가 발생했습니다: {str(e)}"
        )


@router.get("/history/{user_id}/{session_id}", response_model=ConversationHistory, summary="대화 히스토리 조회")
async def get_conversation_history(user_id: str, session_id: str):
    """
    특정 사용자의 세션별 대화 히스토리를 조회합니다.
    
    - **user_id**: 사용자 ID
    - **session_id**: 세션 ID
    """
    try:
        history = memory_manager.get_conversation_history(user_id, session_id)
        
        return ConversationHistory(
            history=history,
            session_id=session_id,
            user_id=user_id,
            total_messages=len(history)
        )
        
    except Exception as e:
        logger.error(f"히스토리 조회 중 에러 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"히스토리 조회 중 에러가 발생했습니다: {str(e)}"
        )


@router.post("/new-session/{user_id}", response_model=SessionResponse, summary="새 세션 생성")
async def create_new_session(user_id: str):
    """
    사용자의 새로운 채팅 세션을 생성합니다.
    
    - **user_id**: 사용자 ID
    """
    try:
        session_id = str(uuid.uuid4())
        
        return SessionResponse(
            session_id=session_id,
            user_id=user_id,
            created_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"세션 생성 중 에러 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"세션 생성 중 에러가 발생했습니다: {str(e)}"
        ) 