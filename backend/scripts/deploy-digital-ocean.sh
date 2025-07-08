#!/bin/bash
# Script de despliegue para Digital Ocean Droplet

echo "🌊 Configurando despliegue para Digital Ocean..."

# Verificar archivos necesarios
if [ ! -f "../app/main.py" ]; then
    echo "❌ No se encuentra main.py. Ejecutar desde scripts/"
    exit 1
fi

# Crear variables de entorno
cat > ../.env.example << 'EOF'
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# File Configuration
MAX_FILE_SIZE=10485760

# Production Configuration
PORT=8000
EOF

# Crear systemd service file
cat > proxy-contabilidad.service << 'EOF'
[Unit]
Description=Proxy Contabilidad Backend
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/var/www/proxy-contabilidad/backend
Environment=PATH=/var/www/proxy-contabilidad/backend/venv/bin
ExecStart=/var/www/proxy-contabilidad/backend/venv/bin/gunicorn app.main:app -c config/gunicorn.conf.py
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Crear nginx configuration
cat > nginx-proxy-contabilidad.conf << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        access_log off;
    }
}
EOF

# Crear script de instalación
cat > install-digital-ocean.sh << 'EOF'
#!/bin/bash
# Script de instalación para Digital Ocean (ejecutar como root)

echo "🔧 Instalando dependencias del sistema..."

# Actualizar sistema
apt update && apt upgrade -y

# Instalar dependencias
apt install -y python3 python3-pip python3-venv nginx git ufw

# Crear usuario para la aplicación
useradd -m -s /bin/bash www-data || true

# Configurar firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80
ufw allow 443
ufw --force enable

# Crear directorio de aplicación
mkdir -p /var/www/proxy-contabilidad
chown www-data:www-data /var/www/proxy-contabilidad

echo "✅ Instalación base completada"
echo "🔄 Ahora sube el código y configura el servicio"
EOF

chmod +x install-digital-ocean.sh

echo "✅ Archivos de configuración creados para Digital Ocean"
echo ""
echo "🚀 Pasos para desplegar en Digital Ocean:"
echo "1. Crear droplet Ubuntu 22.04"
echo "2. Configurar SSH keys"
echo "3. Ejecutar script de instalación"
echo "4. Subir código y configurar variables de entorno"
echo "5. Configurar dominio y SSL"
echo ""
echo "📝 Comandos útiles:"
echo "  - Estado: sudo systemctl status proxy-contabilidad"
echo "  - Logs: sudo journalctl -u proxy-contabilidad -f"
echo "  - Reiniciar: sudo systemctl restart proxy-contabilidad" 