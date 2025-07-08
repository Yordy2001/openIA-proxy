from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class Finding(BaseModel):
    """Model for individual findings in the analysis"""
    type: str  # "error", "warning", "info"
    title: str
    description: str
    location: str
    severity: str  # "high", "medium", "low"
    suggested_fix: str
    sheet: Optional[str] = None
    row: Optional[int] = None


class Recommendation(BaseModel):
    """Model for recommendations"""
    title: str
    description: str
    priority: str  # "high", "medium", "low"
    category: str  # "calculation", "format", "process", "validation"


class AnalysisResponse(BaseModel):
    """Model for analysis response"""
    success: bool = True
    summary: str
    findings: List[Finding]
    recommendations: List[Recommendation]
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None  # Add session_id for chat context


class AnalysisRequest(BaseModel):
    """Model for analysis request"""
    prompt: Optional[str] = None


class ErrorResponse(BaseModel):
    """Model for error responses"""
    error: str
    detail: Optional[str] = None 
