#!/bin/bash
# Quick fix for SQLite permission issues
# Run as root: sudo bash fix_permissions_and_init.sh

set -e

PROJECT_DIR="/var/www/madrasha"
cd "$PROJECT_DIR"

echo "🔧 Fixing permissions and initializing database..."
echo ""

# Remove old instance directory to start fresh
echo "Step 1: Cleaning old instance directory..."
rm -rf instance
rm -f .env

# Create directories with correct permissions from the start
echo "Step 2: Creating instance directory with correct permissions..."
mkdir -p instance logs static/uploads
chown -R www-data:www-data instance logs static
chmod 775 instance  # Write permissions for SQLite
chmod 755 logs static

echo "✅ Directories created with correct ownership"
ls -ld instance

# Create .env file
echo ""
echo "Step 3: Creating .env configuration..."
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
chown www-data:www-data .env
chmod 640 .env

echo "✅ Configuration created"

# Initialize database as www-data user
echo ""
echo "Step 4: Initializing database as www-data user..."
echo "Running: sudo -u www-data venv/bin/python3 init_sqlite_vps.py"
sudo -u www-data venv/bin/python3 init_sqlite_vps.py

# Verify database was created
echo ""
echo "Step 5: Verifying database..."
if [ -f instance/madrasha.db ]; then
    echo "✅ SUCCESS! Database created:"
    ls -lh instance/madrasha.db
    
    # Set final permissions
    chmod 644 instance/madrasha.db
    chown www-data:www-data instance/madrasha.db
    
    echo ""
    echo "🎉 Database initialization complete!"
    echo ""
    echo "Now restart the service:"
    echo "  systemctl restart madrasha"
    echo "  systemctl status madrasha"
else
    echo "❌ FAILED: Database file not created"
    exit 1
fi
