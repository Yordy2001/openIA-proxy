# 🚀 Guía de Despliegue - Proxy Contabilidad

## 📁 Estructura del Proyecto

```
proxy-contabilidad/
├── backend/                 # API FastAPI
│   ├── main.py             # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── chat_models.py      # Modelos de chat
│   ├── session_service.py  # Gestión de sesiones
│   ├── openai_service.py   # Servicio OpenAI
│   ├── gemini_service.py   # Servicio Gemini
│   ├── excel_service.py    # Procesamiento Excel
│   ├── config.py           # Configuración
│   ├── requirements.txt    # Dependencias Python
│   ├── Dockerfile          # Contenedor backend
│   └── tests/              # Pruebas
├── client/                 # Frontend React
│   ├── src/               # Código fuente
│   ├── public/            # Archivos estáticos
│   ├── package.json       # Dependencias Node.js
│   ├── Dockerfile         # Contenedor frontend
│   └── nginx.conf         # Configuración Nginx
├── scripts/               # Scripts de despliegue
│   ├── dev.sh            # Desarrollo local
│   └── deploy.sh         # Despliegue Docker
├── docker-compose.yml    # Orquestación
├── nginx.conf           # Reverse proxy
├── .env.example        # Variables de entorno
└── README.md          # Documentación
```

## 🛠️ Métodos de Despliegue

### 1. Desarrollo Local

```bash
# Clonar repositorio
git clone <repo-url>
cd proxy-contabilidad

# Configurar entorno
cp .env.example .env
# Editar .env con tus API keys

# Ejecutar en desarrollo
./scripts/dev.sh
```

### 2. Docker Compose (Recomendado)

```bash
# Configurar entorno
cp .env.example .env
# Editar .env con tus API keys

# Desplegar con Docker
./scripts/deploy.sh

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

### 3. Kubernetes (Producción)

```bash
# Crear namespace
kubectl create namespace proxy-contabilidad

# Aplicar configuración
kubectl apply -f k8s/

# Ver estado
kubectl get pods -n proxy-contabilidad
```

## 🌐 URLs de Acceso

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 Configuración

### Variables de Entorno Requeridas

```env
# Proveedor de IA
AI_PROVIDER=openai  # o gemini

# OpenAI (si AI_PROVIDER=openai)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

# Gemini (si AI_PROVIDER=gemini)
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-pro

# Configuración de archivos
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=xlsx,xls
```

### Configuración de Producción

```env
# Base de datos (opcional)
DATABASE_URL=postgresql://user:pass@host:5432/db

# Redis para sesiones (opcional)
REDIS_URL=redis://localhost:6379

# Seguridad
SECRET_KEY=tu-clave-secreta-aqui
CORS_ORIGINS=https://tu-dominio.com

# SSL/HTTPS
SSL_CERT_PATH=/path/to/cert.pem
SSL_KEY_PATH=/path/to/key.pem
```

## 📊 Monitoreo

### Health Checks

```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000

# Con Docker
docker-compose ps
```

### Logs

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

## 🔄 Actualizaciones

```bash
# Actualizar código
git pull origin main

# Reconstruir contenedores
docker-compose build --no-cache

# Reiniciar servicios
docker-compose up -d
```

## 🚨 Troubleshooting

### Problemas Comunes

1. **Error de API Key**
   - Verificar .env tiene las API keys correctas
   - Comprobar formato de las keys

2. **Puerto ocupado**
   ```bash
   sudo lsof -i :8000  # Ver qué usa el puerto
   sudo kill -9 <PID>  # Matar proceso
   ```

3. **Contenedores no inician**
   ```bash
   docker-compose down
   docker system prune -f
   docker-compose up --build
   ```

4. **Problemas de CORS**
   - Verificar CORS_ORIGINS en .env
   - Comprobar URL del frontend

### Logs de Depuración

```bash
# Logs detallados
docker-compose logs --tail=100 -f backend

# Entrar al contenedor
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 🔒 Seguridad

### Recomendaciones de Producción

1. **HTTPS**: Configurar certificados SSL
2. **Firewall**: Cerrar puertos innecesarios
3. **API Keys**: Usar variables de entorno seguras
4. **Rate Limiting**: Configurado en nginx.conf
5. **CORS**: Restringir orígenes permitidos

### Backup

```bash
# Backup de configuración
tar -czf backup-$(date +%Y%m%d).tar.gz .env docker-compose.yml

# Backup de logs
docker-compose logs > logs-$(date +%Y%m%d).log
```

## 📈 Escalabilidad

### Múltiples Instancias

```yaml
# En docker-compose.yml
backend:
  deploy:
    replicas: 3
  
frontend:
  deploy:
    replicas: 2
```

### Load Balancer

- Usar nginx como load balancer
- Configurar health checks
- Implementar circuit breakers

## 🎯 Próximos Pasos

- [ ] Configurar CI/CD pipeline
- [ ] Implementar base de datos persistente
- [ ] Agregar cache con Redis
- [ ] Configurar monitoreo con Prometheus
- [ ] Implementar logs estructurados

