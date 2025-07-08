#!/bin/bash
# Script para desarrollo local

echo "🚀 Iniciando desarrollo local..."

# Verificar que .env existe
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    echo "✏️  Por favor edita .env con tus API keys"
    exit 1
fi

# Iniciar backend
echo "🔧 Iniciando backend..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Esperar un momento para que el backend inicie
sleep 5

# Iniciar frontend
echo "⚛️  Iniciando frontend..."
cd client
npm start &
FRONTEND_PID=$!
cd ..

echo "✅ Servicios iniciados:"
echo "   - Backend: http://localhost:8000"
echo "   - Frontend: http://localhost:3000"
echo ""
echo "Presiona Ctrl+C para detener los servicios"

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Capturar señal de interrupción
trap cleanup INT

# Esperar indefinidamente
wait
