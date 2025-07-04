import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Provider selection
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai")  # openai, gemini
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    # Gemini Configuration (Free Tier)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-pro")
    
    # File Configuration
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_EXTENSIONS: set = {".xlsx", ".xls"}
    
    DEFAULT_PROMPT: str = """Actúa como un auditor contable profesional. A continuación, recibirás datos tabulados provenientes de un archivo Excel contable. 

Analiza los datos y realiza lo siguiente:
1. Identifica errores en los cuadres contables
2. Verifica desbalances entre ingresos y egresos
3. Busca inconsistencias en los registros
4. Detecta posibles errores de entrada de datos
5. Revisa que los totales cuadren correctamente

Genera un resumen ejecutivo de hallazgos con formato JSON que incluya:
- Un resumen general
- Una lista de hallazgos específicos con ubicación (hoja y fila si es posible)
- Recomendaciones para corrección

Sé específico y técnico en tu análisis."""


settings = Settings()