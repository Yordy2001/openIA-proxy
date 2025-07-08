from fastapi import HTTPException
from app.core.config import settings
from app.services.ai.openai_service import OpenAIService

# Global AI service instance
ai_service = None


def get_ai_service():
    """Dependency to get AI service"""
    global ai_service
    
    if ai_service is None:
        try:
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY no está configurada")
            ai_service = OpenAIService()
        except Exception as e:
            raise HTTPException(
                status_code=503,
                detail=f"Servicio de OpenAI no está disponible. Error: {str(e)}"
            )
    
    return ai_service 