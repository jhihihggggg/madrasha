#!/bin/bash
# Quick fix script for VPS deployment issues

echo "🔧 Fixing VPS Deployment Issues"
echo "================================"

# Fix 1: Git ownership issue
echo "1️⃣ Fixing git ownership..."
git config --global --add safe.directory /var/www/madrasha
echo "✓ Git ownership fixed"

# Fix 2: Pull latest code
echo "2️⃣ Pulling latest code..."
git pull origin main
echo "✓ Code updated"

# Fix 3: Ensure .env is correct
echo "3️⃣ Checking .env file..."
if [ -f .env ]; then
    echo "✓ .env exists"
    cat .env
else
    echo "⚠️  Creating .env file..."
    cat > .env << 'EOF'
FLASK_ENV=production
DATABASE_URL=sqlite:///instance/madrasha.db
SMS_API_KEY=gsOKLO6XtKsANCvgPHNt
SMS_API_URL=http://bulksmsbd.net/api/smsapi
SMS_SENDER_ID=8809617628909
EOF
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    echo "SECRET_KEY=$SECRET_KEY" >> .env
    echo "✓ .env created"
fi

# Fix 4: Create necessary directories
echo "4️⃣ Creating directories..."
mkdir -p instance logs static/uploads
chown -R www-data:www-data instance logs static
echo "✓ Directories created"

# Fix 5: Initialize database
echo "5️⃣ Initializing database..."
if [ -f "venv/bin/python3" ]; then
    source venv/bin/activate
    python3 create_default_users.py
    deactivate
    echo "✓ Database initialized"
else
    echo "⚠️  Virtual environment not found, skipping DB init"
fi

# Fix 6: Set correct permissions
echo "6️⃣ Setting permissions..."
chown -R www-data:www-data /var/www/madrasha
chmod +x *.sh
echo "✓ Permissions set"

# Fix 7: Reload systemd and start service
echo "7️⃣ Starting madrasha service..."
systemctl daemon-reload
systemctl enable madrasha.service
systemctl restart madrasha.service
sleep 3
echo "✓ Service commands executed"

# Fix 8: Check service status
echo ""
echo "📊 Service Status:"
systemctl status madrasha.service --no-pager -l

echo ""
echo "🔍 Checking application health..."
sleep 2
curl -s http://localhost:8000/health || echo "⚠️  Health check failed"

echo ""
echo "📝 Recent service logs:"
journalctl -u madrasha.service -n 20 --no-pager

echo ""
echo "================================"
echo "✅ Fix script complete!"
echo "================================"
echo ""
echo "If service is still not running, check logs:"
echo "  journalctl -u madrasha.service -f"
echo ""
echo "Manual start if needed:"
echo "  systemctl start madrasha.service"
