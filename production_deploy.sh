#!/bin/bash
# Madrasha Ummul Qura VPS Production Deployment Script
# Domain: madrasaummulqura.com
# Run this script on your Ubuntu VPS after cloning from GitHub

set -e  # Exit on any error

echo "🕌 Madrasha Ummul Qura Production Deployment"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration - MODIFY THESE FOR YOUR VPS
PROJECT_DIR="/var/www/madrasha"
DOMAIN="madrasaummulqura.com"
VENV_DIR="$PROJECT_DIR/venv"
SERVICE_NAME="madrasha"
APP_USER="www-data"  # User to run the application
DB_DIR="$PROJECT_DIR/instance"
BACKUP_DIR="$PROJECT_DIR/backups"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "${BLUE}📍 Deployment Directory: $PROJECT_DIR${NC}"
echo -e "${BLUE}🌐 Domain: $DOMAIN${NC}"
echo ""

# Step 1: Stop existing services
echo -e "${YELLOW}Step 1: Stopping existing services...${NC}"
systemctl stop $SERVICE_NAME 2>/dev/null || true
pkill -f "gunicorn.*madrasha" || true
pkill -f "python.*app.py" || true
echo -e "${GREEN}✓ Services stopped${NC}"

# Step 2: Navigate to project directory
echo -e "${YELLOW}Step 2: Setting up project directory...${NC}"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Creating project directory..."
    mkdir -p $PROJECT_DIR
fi
cd $PROJECT_DIR
echo -e "${GREEN}✓ Current directory: $(pwd)${NC}"

# Step 3: Create necessary directories
echo -e "${YELLOW}Step 3: Creating necessary directories...${NC}"
mkdir -p $DB_DIR
mkdir -p $BACKUP_DIR
mkdir -p static/uploads
mkdir -p flask_session
mkdir -p logs
echo -e "${GREEN}✓ Directories created${NC}"

# Step 4: Pull/Clone code from GitHub
echo -e "${YELLOW}Step 4: Getting latest code...${NC}"
if [ -d ".git" ]; then
    echo "Pulling latest code from GitHub..."
    git fetch origin
    git pull origin main
else
    echo -e "${RED}⚠️  No git repository found!${NC}"
    echo "Please clone your repository first:"
    echo "  cd /var/www"
    echo "  git clone https://github.com/yourusername/madrasha.git"
    exit 1
fi
echo -e "${GREEN}✓ Code updated${NC}"

# Step 5: Set up Python virtual environment
echo -e "${YELLOW}Step 5: Setting up Python virtual environment...${NC}"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source $VENV_DIR/bin/activate
echo -e "${GREEN}✓ Virtual environment ready${NC}"

# Step 6: Upgrade pip
echo -e "${YELLOW}Step 6: Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel
echo -e "${GREEN}✓ Pip upgraded${NC}"

# Step 7: Install dependencies
echo -e "${YELLOW}Step 7: Installing Python dependencies...${NC}"
pip install -r requirements.txt
pip install gunicorn gevent  # Production WSGI server
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 8: Set up environment variables
echo -e "${YELLOW}Step 8: Setting up environment file...${NC}"
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env <<EOF
# Production Environment Configuration
FLASK_ENV=production
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Database Configuration (SQLite)
DATABASE_URL=sqlite:///$DB_DIR/madrasha.db

# SMS Configuration (ALREADY HARDCODED IN routes/sms.py - No need to change)
# SMS API is pre-configured with BulkSMSBD credentials
SMS_API_KEY=gsOKLO6XtKsANCvgPHNt
SMS_API_URL=http://bulksmsbd.net/api/smsapi
SMS_SENDER_ID=8809617628909

# Application Settings
APP_NAME=Madrasha Ummul Qura
DOMAIN=$DOMAIN
EOF
    echo -e "${GREEN}✓ Created .env file${NC}"
    echo -e "${GREEN}✓ SMS is already configured (hardcoded in application)${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Step 9: Initialize database
echo -e "${YELLOW}Step 9: Initializing database...${NC}"
export FLASK_ENV=production

# Create database and tables
python3 -c "
from app import create_app
from models import db

app = create_app('production')
with app.app_context():
    db.create_all()
    print('✓ Database tables created')
"

# Create default admin user if needed
python3 create_default_users.py 2>/dev/null || echo "Default users may already exist"

echo -e "${GREEN}✓ Database initialized${NC}"

# Step 10: Set proper permissions
echo -e "${YELLOW}Step 10: Setting file permissions...${NC}"
chown -R $APP_USER:$APP_USER $PROJECT_DIR
chmod -R 755 $PROJECT_DIR
chmod -R 775 $DB_DIR
chmod -R 775 $BACKUP_DIR
chmod -R 775 static/uploads
chmod -R 775 flask_session
chmod -R 775 logs
chmod 600 .env  # Protect environment file
echo -e "${GREEN}✓ Permissions set${NC}"

# Step 11: Create systemd service
echo -e "${YELLOW}Step 11: Creating systemd service...${NC}"
cat > /etc/systemd/system/$SERVICE_NAME.service <<EOF
[Unit]
Description=Madrasha Ummul Qura Flask Application
After=network.target

[Service]
Type=notify
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
Environment="FLASK_ENV=production"
ExecStart=$VENV_DIR/bin/gunicorn --config $PROJECT_DIR/gunicorn_production.conf.py "app:create_app('production')"
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
echo -e "${GREEN}✓ Systemd service created${NC}"

# Step 12: Enable and start service
echo -e "${YELLOW}Step 12: Starting application service...${NC}"
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME
sleep 3
echo -e "${GREEN}✓ Service started${NC}"

# Step 13: Check service status
echo -e "${YELLOW}Step 13: Verifying service...${NC}"
if systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${GREEN}✓ Service is running${NC}"
else
    echo -e "${RED}❌ Service failed to start!${NC}"
    echo "Checking logs..."
    journalctl -u $SERVICE_NAME -n 50 --no-pager
    exit 1
fi

echo ""
echo "=============================================="
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "=============================================="
echo ""
echo "📊 Service Status:"
systemctl status $SERVICE_NAME --no-pager | head -n 10
echo ""
echo "📝 Useful Commands:"
echo "  View logs:        sudo journalctl -u $SERVICE_NAME -f"
echo "  Restart service:  sudo systemctl restart $SERVICE_NAME"
echo "  Stop service:     sudo systemctl stop $SERVICE_NAME"
echo "  Check status:     sudo systemctl status $SERVICE_NAME"
echo ""
echo "🔧 Next Steps:"
echo "  1. Edit .env file with your SMS API credentials:"
echo "     sudo nano $PROJECT_DIR/.env"
echo ""
echo "  2. Set up Nginx reverse proxy (recommended):"
echo "     sudo bash $PROJECT_DIR/setup_nginx.sh"
echo ""
echo "  3. Configure SSL certificate with Let's Encrypt:"
echo "     sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo ""
echo "  4. Test the application:"
echo "     curl http://localhost:5000/health"
echo ""
echo "  5. Access your application:"
echo "     http://$DOMAIN (after Nginx setup)"
echo ""
echo -e "${GREEN}✅ SMS is already configured and ready to use!${NC}"
echo -e "${GREEN}   Provider: BulkSMSBD${NC}"
echo -e "${GREEN}   Sender ID: 8809617628909${NC}"
echo ""
