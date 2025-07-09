# 🚀 Guía de Desarrollo - Proxy Contabilidad

## 📋 Prerrequisitos

### Para desarrollo local:
- **Python 3.8+** con pip
- **Node.js 18+** con npm
- **Git**

### Para desarrollo con Docker:
- **Docker** y **Docker Compose**

## 🔧 Configuración inicial

1. **Clonar el repositorio:**
   ```bash
   git clone [url-del-repo]
   cd proxy-contabilidad
   ```

2. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con tus API keys
   ```

   Variables necesarias:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   MAX_FILE_SIZE=10485760
   REACT_APP_API_URL=http://localhost:8000
   ```

## 🎯 Modos de desarrollo

### 1. **Desarrollo Local (Recomendado)**
```bash
# Ejecutar ambos servicios con hot-reloading
./scripts/dev.sh

# O usar opciones específicas:
./scripts/dev.sh local    # Ambos servicios
./scripts/dev.sh backend  # Solo backend
./scripts/dev.sh frontend # Solo frontend
```

**Características:**
- ✅ Hot-reloading automático en frontend y backend
- ✅ Detección automática de cambios en archivos
- ✅ Logs en tiempo real
- ✅ Instalación automática de dependencias

### 2. **Desarrollo con Docker**
```bash
# Usar Docker Compose para desarrollo
./scripts/dev.sh docker

# O ejecutar directamente:
docker-compose -f docker-compose.dev.yml up --build
```

**Características:**
- ✅ Entorno aislado
- ✅ Volúmenes montados para hot-reloading
- ✅ Configuración de polling para archivos
- ✅ No requiere instalación local de dependencias

## 📱 Acceso a servicios

Una vez iniciado el desarrollo:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Documentación API:** http://localhost:8000/docs
- **Redoc API:** http://localhost:8000/redoc

## 🔄 Hot-reloading

### Frontend (React)
- **Archivos monitoreados:** `src/`, `public/`
- **Recarga automática:** Cambios en JS, CSS, HTML
- **Puerto:** 3000

### Backend (FastAPI)
- **Archivos monitoreados:** `*.py` en `backend/`
- **Recarga automática:** Cambios en Python
- **Puerto:** 8000

## 🛠️ Comandos útiles

### Frontend
```bash
cd client
npm start        # Servidor de desarrollo
npm run dev      # Servidor con variables de entorno
npm run build    # Build para producción
npm test         # Ejecutar tests
```

### Backend
```bash
cd backend
# Con entorno virtual
source venv/bin/activate
uvicorn main:app --reload   # Servidor de desarrollo
python -m pytest           # Ejecutar tests
```

## 📁 Estructura del proyecto

```
proxy-contabilidad/
├── backend/              # API FastAPI
│   ├── app/             # Aplicación modular
│   ├── models.py        # Modelos de datos
│   ├── main.py          # Punto de entrada
│   └── requirements.txt # Dependencias Python
├── client/              # Frontend React
│   ├── src/            # Código fuente
│   ├── public/         # Archivos públicos
│   ├── package.json    # Dependencias Node
│   ├── Dockerfile      # Para producción
│   └── Dockerfile.dev  # Para desarrollo
├── scripts/
│   └── dev.sh          # Script de desarrollo
├── docker-compose.yml     # Producción
├── docker-compose.dev.yml # Desarrollo
└── README.md
```

## 🐛 Solución de problemas

### El frontend no se conecta al backend:
1. Verificar que el proxy esté configurado en `client/package.json`
2. Confirmar que `REACT_APP_API_URL` apunte a `http://localhost:8000`
3. Asegurarse de que el backend esté ejecutándose en el puerto 8000

### Hot-reloading no funciona:
1. Verificar que los archivos estén en las carpetas correctas
2. Para Docker: confirmar que los volúmenes estén montados
3. Reiniciar los servicios de desarrollo

### Dependencias desactualizadas:
```bash
# Frontend
cd client && npm install

# Backend
cd backend && pip install -r requirements.txt
```

## 🚀 Despliegue

Para producción, usar:
```bash
docker-compose up --build
```

## 📝 Notas importantes

- **Proxy configurado:** Las peticiones de `/api/*` se envían automáticamente al backend
- **Variables de entorno:** Usar `REACT_APP_` para variables del frontend
- **Hot-reloading:** Funciona para ambos servicios en modo desarrollo
- **Puertos:** Frontend (3000), Backend (8000), Nginx (80)

## 🤝 Contribuir

1. Crear rama para feature: `git checkout -b feature/nueva-funcionalidad`
2. Hacer cambios con hot-reloading activo
3. Probar en ambos modos de desarrollo
4. Crear pull request 