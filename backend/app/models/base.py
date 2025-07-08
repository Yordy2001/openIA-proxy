from typing import List, Optional, Dict, Any
from pydantic import BaseModel

# Base model for all response models
class BaseResponse(BaseModel):
    """Base model for all API responses"""
    success: bool = True
    error: Optional[str] = None

class ErrorResponse(BaseModel):
    """Model for error responses"""
    error: str
    detail: Optional[str] = None 