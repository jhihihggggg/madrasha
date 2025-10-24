#!/bin/bash
# Nginx Setup Script for Madrasha Ummul Qura
# Run this after the main deployment script

set -e

echo "🌐 Setting up Nginx for Madrasha Ummul Qura"
echo "============================================"

# Configuration
DOMAIN="madrasaummulqura.com"
PROJECT_DIR="/var/www/madrasha"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Install Nginx if not installed
if ! command -v nginx &> /dev/null; then
    echo "📦 Installing Nginx..."
    apt update
    apt install -y nginx
    echo "✓ Nginx installed"
else
    echo "✓ Nginx already installed"
fi

# Create Nginx configuration
echo "📝 Creating Nginx configuration..."
cat > /etc/nginx/sites-available/madrasha <<'EOF'
# Madrasha Ummul Qura Nginx Configuration

server {
    listen 80;
    listen [::]:80;
    server_name madrasaummulqura.com www.madrasaummulqura.com;

    # Increase buffer sizes for large requests
    client_max_body_size 20M;
    client_body_buffer_size 128k;

    # Logging
    access_log /var/log/nginx/madrasha_access.log;
    error_log /var/log/nginx/madrasha_error.log;

    # Static files
    location /static {
        alias /var/www/madrasha/static/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Uploaded files
    location /uploads {
        alias /var/www/madrasha/static/uploads;
        expires 7d;
        add_header Cache-Control "public";
    }

    # Proxy to Gunicorn
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
        
        # WebSocket support (if needed in future)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
EOF

# Enable the site
echo "🔗 Enabling Nginx site..."
ln -sf /etc/nginx/sites-available/madrasha /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default  # Remove default site

# Test Nginx configuration
echo "✓ Testing Nginx configuration..."
nginx -t

# Restart Nginx
echo "♻️  Restarting Nginx..."
systemctl restart nginx
systemctl enable nginx

echo ""
echo "============================================"
echo "✅ Nginx Setup Complete!"
echo "============================================"
echo ""
echo "📊 Nginx Status:"
systemctl status nginx --no-pager | head -n 5
echo ""
echo "🌐 Your site should now be accessible at:"
echo "   http://$DOMAIN"
echo "   http://www.$DOMAIN"
echo ""
echo "🔒 Next Step: Set up SSL with Let's Encrypt"
echo "   Run: sudo bash $PROJECT_DIR/setup_ssl.sh"
echo ""
echo "📝 Useful Commands:"
echo "   Test config:  sudo nginx -t"
echo "   Reload:       sudo systemctl reload nginx"
echo "   Restart:      sudo systemctl restart nginx"
echo "   View logs:    sudo tail -f /var/log/nginx/madrasha_error.log"
echo ""
