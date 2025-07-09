from typing import List, Optional, Dict, Any, Union
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
    success: bool
    summary: str
    findings: List[Finding]
    recommendations: List[Recommendation]
    metadata: Dict[str, Any]
    error: Optional[str] = None
    session_id: Optional[str] = None


class ErrorResponse(BaseModel):
    """Model for error responses"""
    error: str
    detail: Optional[str] = None
    status_code: int = 500


# Nuevos modelos para tabla editable
class ExcelCellData(BaseModel):
    """Model for individual cell data"""
    value: Union[str, int, float, None]
    type: str  # "text", "number", "date", "formula"
    editable: bool = True
    row: int
    column: int
    column_name: str


class ExcelSheetData(BaseModel):
    """Model for sheet data"""
    sheet_name: str
    columns: List[str]
    rows: List[Dict[str, Union[str, int, float, None]]]
    shape: List[int]  # [rows, columns]
    numeric_columns: List[str]


class ExcelStructuredData(BaseModel):
    """Model for structured Excel data"""
    filename: str
    sheets: List[ExcelSheetData]
    metadata: Dict[str, Any]


class EditCellRequest(BaseModel):
    """Model for editing cell data"""
    sheet_name: str
    row: int
    column: str
    value: Union[str, int, float, None]


class DownloadRequest(BaseModel):
    """Model for download request"""
    filename: str
    sheets: List[ExcelSheetData] 
