from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import asyncio
from contextlib import asynccontextmanager

from models import AnalysisResponse, ErrorResponse
from excel_service import ExcelProcessor
from openai_service import OpenAIService
from gemini_service import GeminiService
from config import settings


# Initialize services
excel_processor = ExcelProcessor()
ai_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the application"""
    global ai_service
    try:
        # Initialize AI service based on provider
        if settings.AI_PROVIDER == "gemini":
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY no está configurada")
            ai_service = GeminiService(settings.GEMINI_API_KEY, settings.GEMINI_MODEL)
            print(f"🔮 Inicializando Gemini con modelo: {settings.GEMINI_MODEL}")
        else:  # Default to OpenAI
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY no está configurada")
            ai_service = OpenAIService()
            print(f"🤖 Inicializando OpenAI con modelo: {settings.OPENAI_MODEL}")
        
        # Test connection
        if ai_service.test_connection():
            print(f"✅ Conexión con {settings.AI_PROVIDER} establecida correctamente")
        else:
            print(f"⚠️  Advertencia: No se pudo conectar con {settings.AI_PROVIDER}")
        
        yield
    except Exception as e:
        print(f"❌ Error al inicializar {settings.AI_PROVIDER}: {e}")
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
            detail=f"Servicio de IA ({settings.AI_PROVIDER}) no está disponible. Verifique la configuración."
        )
    return ai_service


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "message": "Proxy Contabilidad API está funcionando correctamente",
        "version": "1.0.0",
        "ai_provider": settings.AI_PROVIDER,
        "endpoints": {
            "analyze": "/analyze",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    health_status = {
        "status": "healthy",
        "ai_provider": settings.AI_PROVIDER,
        "services": {
            "excel_processor": "available",
            "ai_service": "unknown"
        },
        "configuration": {
            "max_file_size": f"{settings.MAX_FILE_SIZE / (1024*1024):.1f}MB",
            "allowed_extensions": list(settings.ALLOWED_EXTENSIONS),
        }
    }
    
    # Add provider-specific config
    if settings.AI_PROVIDER == "openai":
        health_status["configuration"]["model"] = settings.OPENAI_MODEL
    elif settings.AI_PROVIDER == "gemini":
        health_status["configuration"]["model"] = settings.GEMINI_MODEL
    
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
        
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
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