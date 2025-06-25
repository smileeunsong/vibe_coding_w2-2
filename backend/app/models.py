from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class ChatRequest(BaseModel):
    """채팅 요청 데이터 모델"""
    message: str = Field(..., min_length=1, max_length=1000, description="사용자 메시지")
    user_id: str = Field(..., description="사용자 ID")
    session_id: Optional[str] = Field(None, description="세션 ID (선택사항, 없으면 자동 생성)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "안녕하세요! 도움이 필요합니다.",
                "user_id": "user123",
                "session_id": "session456"
            }
        }
    )


class ChatResponse(BaseModel):
    """채팅 응답 데이터 모델"""
    response: str = Field(..., description="AI 응답 메시지")
    session_id: str = Field(..., description="세션 ID")
    context_used: bool = Field(default=False, description="이전 대화 컨텍스트 사용 여부")
    timestamp: datetime = Field(default_factory=datetime.now, description="응답 생성 시간")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "response": "안녕하세요! 무엇을 도와드릴까요?",
                "session_id": "session456",
                "context_used": True,
                "timestamp": "2024-01-01T12:00:00"
            }
        }
    )


class SessionResponse(BaseModel):
    """세션 응답 데이터 모델"""
    session_id: str = Field(..., description="생성된 세션 ID")
    user_id: str = Field(..., description="사용자 ID")
    created_at: datetime = Field(default_factory=datetime.now, description="세션 생성 시간")


class ConversationHistory(BaseModel):
    """대화 히스토리 데이터 모델"""
    history: List[Dict[str, Any]] = Field(..., description="대화 히스토리 목록")
    session_id: str = Field(..., description="세션 ID")
    user_id: str = Field(..., description="사용자 ID")
    total_messages: int = Field(..., description="총 메시지 수")


class ErrorResponse(BaseModel):
    """에러 응답 데이터 모델"""
    error: str = Field(..., description="에러 메시지")
    detail: Optional[str] = Field(None, description="에러 상세 정보")
    timestamp: datetime = Field(default_factory=datetime.now, description="에러 발생 시간") 