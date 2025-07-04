# Proxy Contabilidad API

Un backend inteligente en Python usando FastAPI que sirve como proxy para analizar archivos contables de Excel y detectar errores en cuadres contables usando OpenAI ChatGPT.

## 🚀 Características

- **Análisis Inteligente**: Utiliza OpenAI GPT-4 para análisis profesional de datos contables
- **Múltiples Archivos**: Soporte para análisis de uno o varios archivos Excel simultáneamente
- **Formato Estructurado**: Respuestas JSON estructuradas con hallazgos y recomendaciones
- **Validación Robusta**: Validación de archivos, tamaños y formatos
- **API RESTful**: Endpoints bien documentados y compatibles con cualquier cliente
- **Escalable**: Diseñado como microservicio agnóstico al lenguaje

## 📋 Requisitos

- Python 3.8+
- Cuenta OpenAI con API key
- Archivos Excel (.xlsx, .xls)

## 🔧 Instalación

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd proxy-contabilidad
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**:
```bash
# Copiar archivo de ejemplo
cp config.env.example .env

# Editar .env con tu API key de OpenAI
OPENAI_API_KEY=your_actual_api_key_here
```

## 🚀 Uso

### Iniciar el servidor

```bash
# Desarrollo
python main.py

# Producción con uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

La API estará disponible en `http://localhost:8000`

### Documentación interactiva

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📡 Endpoints

### `GET /`
Health check básico

### `GET /health`
Health check detallado con estado de servicios

### `POST /analyze`
Endpoint principal para análisis de archivos contables

**Parámetros**:
- `files`: Archivos Excel (multipart/form-data)
- `prompt`: Prompt personalizado (opcional)

**Respuesta**:
```json
{
  "summary": "Análisis completado. Se encontraron 2 errores de cuadre.",
  "findings": [
    {
      "sheet": "General",
      "row": 18,
      "description": "El total de ingresos ($1234.00) no cuadra con el monto registrado en caja ($1000.00)"
    }
  ],
  "recommendations": "Verificar los registros de movimientos entre fechas específicas."
}
```

## 🔍 Ejemplos de Uso

### cURL

```bash
# Analizar un archivo
curl -X POST "http://localhost:8000/analyze" \
  -F "files=@contabilidad.xlsx" \
  -F "prompt=Analiza especialmente los balances de caja"

# Analizar múltiples archivos
curl -X POST "http://localhost:8000/analyze" \
  -F "files=@balance.xlsx" \
  -F "files=@ingresos.xlsx" \
  -F "files=@egresos.xlsx"
```

### Python

```python
import requests

# Análisis básico
with open('contabilidad.xlsx', 'rb') as f:
    files = {'files': f}
    response = requests.post('http://localhost:8000/analyze', files=files)
    result = response.json()
    print(result)

# Con prompt personalizado
files = {'files': open('balance.xlsx', 'rb')}
data = {'prompt': 'Enfócate en detectar errores de suma y resta'}
response = requests.post('http://localhost:8000/analyze', files=files, data=data)
```

### JavaScript/Node.js

```javascript
const FormData = require('form-data');
const fs = require('fs');

const form = new FormData();
form.append('files', fs.createReadStream('contabilidad.xlsx'));
form.append('prompt', 'Analiza los cuadres contables detalladamente');

fetch('http://localhost:8000/analyze', {
  method: 'POST',
  body: form
})
.then(response => response.json())
.then(data => console.log(data));
```

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `OPENAI_API_KEY` | API key de OpenAI | *Requerido* |
| `OPENAI_MODEL` | Modelo GPT a usar | `gpt-4o` |
| `OPENAI_BASE_URL` | URL base de OpenAI | `https://api.openai.com/v1` |
| `MAX_FILE_SIZE` | Tamaño máximo de archivo (bytes) | `10485760` (10MB) |

### Personalización del Prompt

El sistema incluye un prompt profesional predeterminado, pero puedes usar prompts personalizados:

```python
custom_prompt = """
Actúa como un contador senior especializado en auditoría.
Analiza estos datos contables y enfócate en:
1. Inconsistencias en cuentas por cobrar
2. Errores en depreciaciones
3. Desbalances en el flujo de caja
Sé muy detallado en tus observaciones.
"""
```

## 🐳 Docker (Opcional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔒 Seguridad

- Validación de tipos de archivo
- Límites de tamaño de archivo
- Sanitización de datos de entrada
- Manejo seguro de errores

## 📊 Casos de Uso

1. **Auditoría Contable**: Detectar inconsistencias en balances
2. **Revisión de Cuadres**: Validar que ingresos y egresos cuadren
3. **Control de Calidad**: Verificar entrada de datos contables
4. **Análisis Financiero**: Identificar patrones inusuales en registros

## 🛠️ Integración con Mastra.io

```javascript
// Ejemplo de integración con Mastra.io
const mastra = require('@mastra/core');

const accountingAnalyzer = mastra.createTool({
  name: 'accounting-analyzer',
  url: 'http://localhost:8000/analyze',
  method: 'POST',
  inputSchema: {
    files: 'file[]',
    prompt: 'string?'
  }
});

// Uso en un workflow
await accountingAnalyzer.execute({
  files: [excelFile],
  prompt: 'Analiza los cuadres de fin de mes'
});
```

## 🚨 Solución de Problemas

### Error "OpenAI API key not found"
- Verificar que `OPENAI_API_KEY` esté configurada en `.env`
- Comprobar que el archivo `.env` esté en la raíz del proyecto

### Error "File too large"
- Ajustar `MAX_FILE_SIZE` en configuración
- Comprimir archivos Excel antes de enviar

### Error "Invalid file format"
- Usar solo archivos `.xlsx` o `.xls`
- Verificar que el archivo no esté corrupto

## 📈 Monitoreo

El endpoint `/health` proporciona información sobre el estado del sistema:

```json
{
  "status": "healthy",
  "services": {
    "excel_processor": "available",
    "openai_service": "available"
  },
  "configuration": {
    "max_file_size": "10.0MB",
    "allowed_extensions": [".xlsx", ".xls"],
    "openai_model": "gpt-4o"
  }
}
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles. 