from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
from contextlib import asynccontextmanager

from models import AnalysisResponse, ErrorResponse
from chat_models import ChatRequest, ChatResponse, SessionListResponse, ChatMessage
from session_service import session_service
from excel_service import ExcelProcessor
from openai_service import OpenAIService
from config import settings


# Initialize services
excel_processor = ExcelProcessor()
ai_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the application"""
    global ai_service
    try:
        # Initialize OpenAI service
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no está configurada")
        
        ai_service = OpenAIService()
        print(f"🤖 Inicializando OpenAI con modelo: {settings.OPENAI_MODEL}")
        
        # Test connection
        if ai_service.test_connection():
            print("✅ Conexión con OpenAI establecida correctamente")
        else:
            print("⚠️  Advertencia: No se pudo conectar con OpenAI")
        
        yield
    except Exception as e:
        print(f"❌ Error al inicializar OpenAI: {e}")
        yield
    finally:
        print("🔄 Cerrando aplicación...")


# Create FastAPI app
app = FastAPI(
    title="Proxy Contabilidad API",
    description="API para analizar archivos contables de Excel usando inteligencia artificial",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_ai_service():
    """Dependency to get AI service"""
    if ai_service is None:
        raise HTTPException(
            status_code=503,
            detail="Servicio de IA no está disponible. Verifique la configuración."
        )
    return ai_service


@app.get("/", tags=["Health"])
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


@app.get("/health", tags=["Health"])
async def health_check():
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
        if ai_service and ai_service.test_connection():
            health_status["services"]["ai_service"] = "available"
        else:
            health_status["services"]["ai_service"] = "unavailable"
            health_status["status"] = "degraded"
    except Exception:
        health_status["services"]["ai_service"] = "error"
        health_status["status"] = "degraded"
    
    return health_status


@app.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_accounting_files(
    files: List[UploadFile] = File(..., description="Archivos Excel para analizar"),
    prompt: Optional[str] = Form(None, description="Prompt personalizado para el análisis"),
    ai_svc = Depends(get_ai_service)
):
    """
    Analizar archivos contables de Excel para detectar errores en cuadres contables.
    
    - **files**: Uno o más archivos Excel (.xlsx, .xls)
    - **prompt**: Prompt personalizado opcional para el análisis
    
    Retorna un análisis estructurado con hallazgos y recomendaciones.
    """
    if not files:
        raise HTTPException(
            status_code=400,
            detail="No se proporcionaron archivos para analizar"
        )
    
    # Validate and process files
    processed_files = []
    
    for file in files:
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Todos los archivos deben tener un nombre"
            )
        
        try:
            # Read file content
            content = await file.read()
            
            # Validate file
            excel_processor.validate_file(
                file.filename,
                len(content),
                settings.MAX_FILE_SIZE
            )
            
            # Store file data
            processed_files.append({
                'filename': file.filename,
                'content': content
            })
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar el archivo {file.filename}: {str(e)}"
            )
    
    try:
        # Process Excel files
        if len(processed_files) == 1:
            excel_data = excel_processor.extract_data_from_excel(
                processed_files[0]['content'],
                processed_files[0]['filename']
            )
        else:
            excel_data = excel_processor.process_multiple_files(processed_files)
        
        # Analyze with AI service
        analysis_result = ai_svc.analyze_accounting_data(
            excel_data,
            prompt or ""
        )
        
        # Create session for chat
        file_names = [f["filename"] for f in processed_files]
        session_id = session_service.create_session(
            analysis_result=analysis_result.dict(),
            excel_data={"data": excel_data, "files": file_names},
            file_names=file_names
        )
        
        # Add session_id to response
        analysis_result.session_id = session_id
        
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_with_analysis(
    chat_request: ChatRequest,
    ai_svc = Depends(get_ai_service)
):
    """
    Chat basado en el análisis previo usando el session_id.
    
    - **session_id**: ID de la sesión del análisis previo
    - **message**: Mensaje del usuario
    
    Permite hacer preguntas sobre el análisis sin re-procesar archivos.
    """
    try:
        # Get session
        session = session_service.get_session(chat_request.session_id)
        if not session:
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada o expirada"
            )
        
        # Add user message to conversation
        user_message = ChatMessage(
            role="user",
            content=chat_request.message
        )
        session_service.add_message(chat_request.session_id, user_message)
        
        # Get conversation context
        context = session_service.get_conversation_context(chat_request.session_id)
        
        # Get AI response
        ai_response = ai_svc.chat_with_context(context, chat_request.message)
        
        # Add AI response to conversation
        ai_message = ChatMessage(
            role="assistant",
            content=ai_response
        )
        session_service.add_message(chat_request.session_id, ai_message)
        
        # Return response
        return ChatResponse(
            success=True,
            response=ai_response,
            session_id=chat_request.session_id,
            conversation_history=session.conversation_history
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el chat: {str(e)}"
        )


@app.get("/sessions", response_model=SessionListResponse, tags=["Sessions"])
async def list_sessions():
    """
    Lista todas las sesiones activas.
    
    Retorna información básica de las sesiones de análisis.
    """
    try:
        sessions = session_service.list_sessions()
        return SessionListResponse(
            sessions=sessions,
            total=len(sessions)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener las sesiones: {str(e)}"
        )


@app.get("/sessions/{session_id}", tags=["Sessions"])
async def get_session_details(session_id: str):
    """
    Obtiene los detalles de una sesión específica.
    
    - **session_id**: ID de la sesión
    """
    try:
        session = session_service.get_session(session_id)
        if not session:
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada"
            )
        
        return {
            "session_id": session.session_id,
            "file_names": session.file_names,
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
            "conversation_history": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in session.conversation_history
            ],
            "analysis_summary": session.analysis_result.get("summary", "No disponible")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener la sesión: {str(e)}"
        )


@app.delete("/sessions/{session_id}", tags=["Sessions"])
async def delete_session(session_id: str):
    """
    Elimina una sesión específica.
    
    - **session_id**: ID de la sesión a eliminar
    """
    try:
        deleted = session_service.delete_session(session_id)
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada"
            )
        
        return {"message": "Sesión eliminada exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar la sesión: {str(e)}"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "detail": str(exc),
            "status_code": 500
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 