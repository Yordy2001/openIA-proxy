from fastapi import APIRouter, Depends
from app.core.config import settings
from app.dependencies import get_ai_service

router = APIRouter()


@router.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Proxy Contabilidad API está funcionando correctamente",
        "version": "1.0.0",
        "ai_provider": "openai",
        "endpoints": {
            "analyze": "/analyze",
            "chat": "/chat",
            "sessions": "/sessions",
            "health": "/health",
            "docs": "/docs"
        }
    }


@router.get("/health")
async def health_check(ai_svc=Depends(get_ai_service)):
    """Detailed health check"""
    health_status = {
        "status": "healthy",
        "ai_provider": "openai",
        "services": {
            "excel_processor": "available",
            "ai_service": "unknown"
        },
        "configuration": {
            "max_file_size": f"{settings.MAX_FILE_SIZE / (1024*1024):.1f}MB",
            "allowed_extensions": list(settings.ALLOWED_EXTENSIONS),
            "model": settings.OPENAI_MODEL
        }
    }
    
    # Test AI service connection
    try:
        if ai_svc and ai_svc.test_connection():
            health_status["services"]["ai_service"] = "available"
        else:
            health_status["services"]["ai_service"] = "unavailable"
            health_status["status"] = "degraded"
    except Exception:
        health_status["services"]["ai_service"] = "error"
        health_status["status"] = "degraded"
    
    return health_status 