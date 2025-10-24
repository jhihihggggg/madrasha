#!/bin/bash
# Complete VPS Deployment Script for Madrasha on Port 8002
# Run as root: sudo bash deploy_vps_8002.sh

set -e

echo "🕌 Madrasha Ummul Qura VPS Deployment (Port 8002)"
echo "=================================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

PROJECT_DIR="/var/www/madrasha"
cd "$PROJECT_DIR"

echo "Step 1: Installing system dependencies..."
apt update
apt install -y python3 python3-pip python3-venv nginx git curl lsof
echo "✅ System dependencies installed"

echo ""
echo "Step 2: Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Python environment ready"

echo ""
echo "Step 3: Creating SQLite database configuration..."
mkdir -p instance logs static/uploads

# Create .env file with SQLite
cat > .env << 'EOF'
FLASK_ENV=production
DATABASE_URL=sqlite:///instance/madrasha.db
SMS_API_KEY=gsOKLO6XtKsANCvgPHNt
SMS_API_URL=http://bulksmsbd.net/api/smsapi
SMS_SENDER_ID=8809617628909
EOF

# Generate SECRET_KEY
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
echo "SECRET_KEY=$SECRET_KEY" >> .env
echo "✅ Configuration file created with SQLite"

echo ""
echo "Step 4: Initializing SQLite database..."
python3 create_default_users.py
echo "✅ SQLite database initialized at instance/madrasha.db"
ls -lh instance/madrasha.db

deactivate

echo ""
echo "Step 5: Setting file permissions..."
chown -R www-data:www-data "$PROJECT_DIR"
chmod 755 instance logs static
chmod 644 instance/madrasha.db
chmod +x *.sh
echo "✅ Permissions set"

echo ""
echo "Step 6: Creating systemd service..."
cat > /etc/systemd/system/madrasha.service << 'SERVICEEOF'
[Unit]
Description=Madrasha Ummul Qura Flask Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/madrasha
Environment="PATH=/var/www/madrasha/venv/bin"
ExecStart=/var/www/madrasha/venv/bin/gunicorn -c /var/www/madrasha/gunicorn_production.conf.py app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEEOF

systemctl daemon-reload
systemctl enable madrasha.service
echo "✅ Systemd service created"

echo ""
echo "Step 7: Configuring Nginx..."
cat > /etc/nginx/sites-available/madrasha << 'NGINXEOF'
server {
    listen 80;
    listen [::]:80;
    server_name madrasaummulqura.com www.madrasaummulqura.com;

    client_max_body_size 20M;
    client_body_buffer_size 128k;

    access_log /var/log/nginx/madrasha_access.log;
    error_log /var/log/nginx/madrasha_error.log;

    location /static {
        alias /var/www/madrasha/static/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /uploads {
        alias /var/www/madrasha/static/uploads;
        expires 7d;
        add_header Cache-Control "public";
    }

    location / {
        proxy_pass http://127.0.0.1:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
NGINXEOF

ln -sf /etc/nginx/sites-available/madrasha /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
echo "✅ Nginx configured for port 8002"

echo ""
echo "Step 8: Starting application..."
systemctl restart madrasha.service
sleep 5
echo "✅ Application started"

echo ""
echo "=================================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=================================================="
echo ""
echo "📊 Status Check:"
systemctl status madrasha.service --no-pager -l | head -15
echo ""
echo "🔍 Port Check:"
lsof -i :8002 || echo "⚠️  Port 8002 not listening yet (may need a moment)"
echo ""
echo "🗄️  Database:"
ls -lh instance/madrasha.db
echo ""
echo "🌐 Access your site:"
echo "   http://madrasaummulqura.com"
echo "   http://YOUR_VPS_IP"
echo ""
echo "📱 Default Login:"
echo "   Admin: 01712345678 / admin123"
echo "   Teacher: 01812345678 / teacher123"
echo ""
echo "🔧 Useful Commands:"
echo "   Service: systemctl status madrasha.service"
echo "   Logs: journalctl -u madrasha.service -f"
echo "   Test: curl http://localhost:8002/health"
echo "   Restart: systemctl restart madrasha.service"
echo ""
echo "🔒 Next: Setup SSL with: bash setup_ssl.sh"
echo ""
