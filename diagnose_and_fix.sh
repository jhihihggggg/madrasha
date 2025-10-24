#!/bin/bash
# Comprehensive diagnostic and fix script for 502 errors

echo "🔍 DIAGNOSING 502 ERROR"
echo "======================="

# 1. Check if service is running
echo ""
echo "1️⃣ Checking madrasha service status..."
systemctl is-active madrasha.service
if [ $? -eq 0 ]; then
    echo "✅ Service is running"
else
    echo "❌ Service is NOT running"
    echo "📋 Service status:"
    systemctl status madrasha.service --no-pager -l
    echo ""
    echo "📋 Recent logs:"
    journalctl -u madrasha.service -n 30 --no-pager
fi

# 2. Check if port 8002 is listening
echo ""
echo "2️⃣ Checking if port 8002 is listening..."
if lsof -i :8002 > /dev/null 2>&1; then
    echo "✅ Port 8002 is in use:"
    lsof -i :8002
else
    echo "❌ Port 8002 is NOT listening"
fi

# 3. Test localhost connection
echo ""
echo "3️⃣ Testing localhost:8002..."
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:8002/health || echo "❌ Cannot connect to localhost:8002"

# 4. Check .env file
echo ""
echo "4️⃣ Checking .env configuration..."
if [ -f .env ]; then
    echo "✅ .env exists"
    echo "Contents (without SECRET_KEY):"
    grep -v SECRET_KEY .env
else
    echo "❌ .env NOT found"
fi

# 5. Check database
echo ""
echo "5️⃣ Checking database..."
if [ -f instance/madrasha.db ]; then
    echo "✅ Database exists"
    ls -lh instance/madrasha.db
else
    echo "❌ Database NOT found at instance/madrasha.db"
fi

# 6. Check Python virtual environment
echo ""
echo "6️⃣ Checking Python environment..."
if [ -f venv/bin/python3 ]; then
    echo "✅ Virtual environment exists"
    venv/bin/python3 --version
else
    echo "❌ Virtual environment NOT found"
fi

# 7. Check Nginx config
echo ""
echo "7️⃣ Checking Nginx configuration..."
nginx -t

# 8. Check permissions
echo ""
echo "8️⃣ Checking file permissions..."
ls -la instance/ 2>/dev/null || echo "⚠️  instance/ directory not found"

echo ""
echo "======================="
echo "🔧 APPLYING FIXES"
echo "======================="

# Fix 1: Reset git and pull latest
echo ""
echo "Fix 1: Getting latest code..."
git reset --hard origin/main
git pull origin main

# Fix 2: Ensure .env is correct
echo ""
echo "Fix 2: Setting up .env..."
cat > .env << 'ENVEOF'
FLASK_ENV=production
DATABASE_URL=sqlite:///instance/madrasha.db
SMS_API_KEY=gsOKLO6XtKsANCvgPHNt
SMS_API_URL=http://bulksmsbd.net/api/smsapi
SMS_SENDER_ID=8809617628909
ENVEOF

SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || echo "CHANGE_THIS_SECRET_KEY_IN_PRODUCTION")
echo "SECRET_KEY=$SECRET_KEY" >> .env
echo "✅ .env configured"

# Fix 3: Create directories
echo ""
echo "Fix 3: Creating directories..."
mkdir -p instance logs static/uploads
chmod 755 instance logs static
echo "✅ Directories created"

# Fix 4: Install dependencies
echo ""
echo "Fix 4: Installing Python dependencies..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Fix 5: Initialize database
echo ""
echo "Fix 5: Initializing database..."
python3 create_default_users.py
deactivate
echo "✅ Database initialized"

# Fix 6: Set permissions
echo ""
echo "Fix 6: Setting permissions..."
chown -R www-data:www-data /var/www/madrasha
chmod +x *.sh
echo "✅ Permissions set"

# Fix 7: Create systemd service
echo ""
echo "Fix 7: Setting up systemd service..."
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
echo "✅ Systemd service configured"

# Fix 8: Start the service
echo ""
echo "Fix 8: Starting madrasha service..."
systemctl stop madrasha.service 2>/dev/null
sleep 2
systemctl start madrasha.service
sleep 3
echo "✅ Service start command executed"

echo ""
echo "======================="
echo "🔍 VERIFICATION"
echo "======================="

# Verify service
echo ""
echo "Service status:"
systemctl status madrasha.service --no-pager -l | head -20

# Verify port
echo ""
echo "Port 8002 status:"
lsof -i :8002 || echo "⚠️  Port 8002 not listening"

# Test connection
echo ""
echo "Testing localhost:8002..."
sleep 2
curl -v http://localhost:8002/health 2>&1 | head -20

echo ""
echo "======================="
echo "📝 NEXT STEPS"
echo "======================="
echo ""
echo "If still getting 502 error:"
echo "  1. Check logs: journalctl -u madrasha.service -f"
echo "  2. Check Nginx logs: tail -f /var/log/nginx/madrasha_error.log"
echo "  3. Test manually: curl -v http://localhost:8002/health"
echo ""
echo "To restart service:"
echo "  systemctl restart madrasha.service"
echo ""
