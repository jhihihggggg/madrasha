#!/bin/bash
# SSL Setup Script for Madrasha Ummul Qura using Let's Encrypt
# Run this after Nginx is set up and your domain is pointing to the VPS

set -e

echo "🔒 Setting up SSL for Madrasha Ummul Qura"
echo "=========================================="

# Configuration
DOMAIN="madrasaummulqura.com"
EMAIL="admin@madrasaummulqura.com"  # Change this to your email

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Install Certbot if not installed
if ! command -v certbot &> /dev/null; then
    echo "📦 Installing Certbot..."
    apt update
    apt install -y certbot python3-certbot-nginx
    echo "✓ Certbot installed"
else
    echo "✓ Certbot already installed"
fi

# Check if domain resolves to this server
echo "🔍 Checking DNS resolution..."
SERVER_IP=$(curl -s ifconfig.me)
DOMAIN_IP=$(dig +short $DOMAIN | head -n 1)

echo "Server IP: $SERVER_IP"
echo "Domain IP: $DOMAIN_IP"

if [ "$SERVER_IP" != "$DOMAIN_IP" ]; then
    echo "⚠️  WARNING: Domain does not point to this server!"
    echo "Please update your DNS A record to point to: $SERVER_IP"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Request SSL certificate
echo "📜 Requesting SSL certificate..."
echo "Email for renewal notifications: $EMAIL"

certbot --nginx \
    -d $DOMAIN \
    -d www.$DOMAIN \
    --non-interactive \
    --agree-tos \
    --email $EMAIL \
    --redirect

echo ""
echo "=========================================="
echo "✅ SSL Setup Complete!"
echo "=========================================="
echo ""
echo "🔒 Your site is now secured with HTTPS:"
echo "   https://$DOMAIN"
echo "   https://www.$DOMAIN"
echo ""
echo "📋 Certificate Details:"
certbot certificates
echo ""
echo "♻️  Auto-renewal is configured. Test it with:"
echo "   sudo certbot renew --dry-run"
echo ""
echo "📝 Certificate locations:"
echo "   Certificate: /etc/letsencrypt/live/$DOMAIN/fullchain.pem"
echo "   Private Key: /etc/letsencrypt/live/$DOMAIN/privkey.pem"
echo ""
