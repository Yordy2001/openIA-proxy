from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.api.endpoints import health, analysis, chat, sessions
from app.dependencies import get_ai_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the application"""
    try:
        # Initialize AI service
        ai_service = get_ai_service()
        
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
    description="API para analizar archivos contables de Excel usando OpenAI",
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

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(analysis.router, prefix="/analyze", tags=["Analysis"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=500,
        content={"error": "Error interno del servidor", "detail": str(exc)}
    ) 