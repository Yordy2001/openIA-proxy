#!/bin/bash
# Script de despliegue para VPS/Servidor dedicado

echo "🖥️  Configurando despliegue para VPS..."

# Verificar archivos necesarios
if [ ! -f "main.py" ]; then
    echo "❌ No se encuentra main.py. Ejecutar desde backend/"
    exit 1
fi

# Crear systemd service file
cat > proxy-contabilidad.service << 'EOF'
[Unit]
Description=Proxy Contabilidad Backend
After=network.target

[Service]
Type=exec
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/proxy-contabilidad/backend
Environment=PATH=/home/ubuntu/proxy-contabilidad/venv/bin
ExecStart=/home/ubuntu/proxy-contabilidad/venv/bin/gunicorn main:app -c gunicorn.conf.py
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
    server_name tu-dominio.com;  # Cambia esto por tu dominio
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com;  # Cambia esto por tu dominio
    
    # SSL Configuration
    ssl_certificate /etc/ssl/certs/tu-dominio.crt;
    ssl_certificate_key /etc/ssl/private/tu-dominio.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Client upload limit
    client_max_body_size 50M;
    
    # Proxy to backend
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Health check
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        access_log off;
    }
}
EOF

# Crear script de instalación
cat > install-vps.sh << 'EOF'
#!/bin/bash
# Script de instalación para VPS (ejecutar como root)

echo "🔧 Instalando dependencias del sistema..."

# Actualizar sistema
apt update && apt upgrade -y

# Instalar dependencias
apt install -y python3 python3-pip python3-venv nginx git ufw fail2ban

# Crear usuario para la aplicación
useradd -m -s /bin/bash ubuntu || true

# Configurar firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80
ufw allow 443
ufw --force enable

# Configurar fail2ban
systemctl enable fail2ban
systemctl start fail2ban

# Crear directorio de aplicación
mkdir -p /home/ubuntu/proxy-contabilidad
chown ubuntu:ubuntu /home/ubuntu/proxy-contabilidad

echo "✅ Instalación base completada"
echo "🔄 Ahora ejecuta el script de despliegue como usuario ubuntu"
EOF

chmod +x install-vps.sh

# Crear script de despliegue para usuario ubuntu
cat > deploy-app.sh << 'EOF'
#!/bin/bash
# Script para desplegar la aplicación (ejecutar como usuario ubuntu)

echo "🚀 Desplegando aplicación..."

# Ir al directorio de la aplicación
cd /home/ubuntu/proxy-contabilidad

# Clonar o actualizar código
if [ -d ".git" ]; then
    echo "📥 Actualizando código..."
    git pull origin main
else
    echo "📥 Clonando repositorio..."
    git clone https://github.com/tu-usuario/proxy-contabilidad.git .
fi

# Crear entorno virtual
echo "🐍 Configurando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
cd backend
pip install -r requirements.txt

# Configurar variables de entorno
echo "⚙️  Configurando variables de entorno..."
if [ ! -f ".env" ]; then
    cp config.env.example .env
    echo "✏️  Edita /home/ubuntu/proxy-contabilidad/backend/.env con tus API keys"
fi

# Copiar archivos de configuración
echo "📋 Copiando configuración de systemd..."
sudo cp proxy-contabilidad.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable proxy-contabilidad

# Configurar nginx
echo "🌐 Configurando nginx..."
sudo cp nginx-proxy-contabilidad.conf /etc/nginx/sites-available/proxy-contabilidad
sudo ln -sf /etc/nginx/sites-available/proxy-contabilidad /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

# Iniciar servicio
echo "🔄 Iniciando servicio..."
sudo systemctl start proxy-contabilidad
sudo systemctl status proxy-contabilidad

echo "✅ Despliegue completado!"
echo "🌐 Tu aplicación está disponible en: https://tu-dominio.com"
echo "📊 Estado del servicio: sudo systemctl status proxy-contabilidad"
echo "📝 Logs: sudo journalctl -u proxy-contabilidad -f"
EOF

chmod +x deploy-app.sh

echo "✅ Archivos de configuración creados:"
echo "  - proxy-contabilidad.service (systemd)"
echo "  - nginx-proxy-contabilidad.conf (nginx)"
echo "  - install-vps.sh (instalación inicial)"
echo "  - deploy-app.sh (despliegue de app)"
echo ""
echo "🚀 Pasos para desplegar en VPS:"
echo "1. Sube estos archivos a tu VPS"
echo "2. Ejecuta como root: ./install-vps.sh"
echo "3. Ejecuta como ubuntu: ./deploy-app.sh"
echo "4. Configura SSL certificates"
echo "5. Edita nginx config con tu dominio"
echo ""
echo "📊 Comandos útiles:"
echo "  - Estado: sudo systemctl status proxy-contabilidad"
echo "  - Logs: sudo journalctl -u proxy-contabilidad -f"
echo "  - Reiniciar: sudo systemctl restart proxy-contabilidad"
EOF 