from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from .base import BaseResponse


class ChatMessage(BaseModel):
    """Model for chat messages"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = datetime.now()


class ChatRequest(BaseModel):
    """Model for chat request"""
    session_id: str
    message: str


class ChatResponse(BaseResponse):
    """Model for chat response"""
    response: str
    session_id: str
    conversation_history: List[ChatMessage]


class AnalysisSession(BaseModel):
    """Model for analysis session"""
    session_id: str
    analysis_result: Dict[str, Any]
    excel_data: Dict[str, Any]
    conversation_history: List[ChatMessage]
    created_at: datetime = datetime.now()
    last_activity: datetime = datetime.now()
    file_names: List[str] = []


class SessionListResponse(BaseResponse):
    """Model for session list response"""
    sessions: List[Dict[str, Any]]
    total: int 