from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """채팅 요청 데이터 모델"""
    message: str = Field(..., min_length=1, max_length=1000, description="사용자 메시지")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "안녕하세요! 도움이 필요합니다."
            }
        }
    )


class ChatResponse(BaseModel):
    """채팅 응답 데이터 모델"""
    response: str = Field(..., description="AI 응답 메시지")
    timestamp: datetime = Field(default_factory=datetime.now, description="응답 생성 시간")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "response": "안녕하세요! 무엇을 도와드릴까요?",
                "timestamp": "2024-01-01T12:00:00"
            }
        }
    )


class ErrorResponse(BaseModel):
    """에러 응답 데이터 모델"""
    error: str = Field(..., description="에러 메시지")
    detail: Optional[str] = Field(None, description="에러 상세 정보")
    timestamp: datetime = Field(default_factory=datetime.now, description="에러 발생 시간") 