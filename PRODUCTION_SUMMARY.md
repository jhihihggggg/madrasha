# 📦 Production Deployment Package Summary

## What's Included

Your Madrasha management system is now **production-ready** with complete deployment automation for your VPS at `madrasaummulqura.com`.

---

## 📂 New Files Created

### Deployment Scripts
1. **`production_deploy.sh`** - Main deployment automation script
   - Sets up virtual environment
   - Installs dependencies
   - Initializes SQLite database
   - Creates systemd service
   - Configures permissions
   - Starts the application

2. **`setup_nginx.sh`** - Nginx reverse proxy setup
   - Installs Nginx
   - Configures reverse proxy to Gunicorn
   - Sets up static file serving
   - Enables the site

3. **`setup_ssl.sh`** - SSL/HTTPS certificate setup
   - Installs Certbot
   - Obtains Let's Encrypt certificate
   - Configures auto-renewal
   - Forces HTTPS redirect

4. **`backup_database.sh`** - Automated database backup
   - Creates compressed backups
   - Retains 30 days of backups
   - Can be run via cron for daily backups

5. **`check_health.sh`** - Application health monitoring
   - Checks service status
   - Tests application endpoints
   - Auto-restarts if unhealthy
   - Monitors disk space

### Configuration Files
6. **`gunicorn_production.conf.py`** - Production WSGI server config
   - Multi-worker setup
   - Gevent for concurrency
   - Logging configuration
   - Performance tuning

### Documentation
7. **`QUICK_START.md`** - Quick deployment guide
8. **`DEPLOYMENT_CHECKLIST.md`** - Complete deployment checklist
9. **`VPS_DEPLOYMENT_GUIDE.md`** (existing) - Full deployment documentation

### Updated Files
10. **`requirements.txt`** - Added production dependencies (gunicorn, gevent)
11. **`config.py`** (existing) - Already configured for production SQLite

---

## 🚀 How to Deploy

### On Your Ubuntu VPS:

```bash
# 1. Clone from GitHub
cd /var/www
sudo git clone https://github.com/jhihihggggg/madrasha.git
cd madrasha

# 2. Make scripts executable
sudo chmod +x *.sh

# 3. Deploy
sudo bash production_deploy.sh

# 4. Setup Nginx
sudo bash setup_nginx.sh

# 5. Setup SSL (after DNS points to VPS)
sudo bash setup_ssl.sh

# 6. Setup automatic backups
sudo crontab -e
# Add: 0 2 * * * /var/www/madrasha/backup_database.sh >> /var/www/madrasha/logs/backup.log 2>&1

# 7. Setup health monitoring (optional)
sudo crontab -e
# Add: */5 * * * * /var/www/madrasha/check_health.sh >> /var/www/madrasha/logs/health_check.log 2>&1
```

---

## 🗂️ Production Directory Structure

```
/var/www/madrasha/
├── app.py                          # Flask application
├── config.py                       # Configuration (SQLite)
├── models.py                       # Database models
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (created during deploy)
│
├── instance/                      # Database directory
│   └── madrasha.db               # SQLite database file
│
├── backups/                       # Database backups
│   └── madrasha_backup_*.db.gz   # Compressed backups
│
├── logs/                          # Application logs
│   ├── gunicorn_access.log       # Access logs
│   ├── gunicorn_error.log        # Error logs
│   ├── backup.log                # Backup logs
│   └── health_check.log          # Health check logs
│
├── static/                        # Static files
│   ├── static/                   # CSS, JS, images
│   └── uploads/                  # User uploads
│
├── templates/                     # HTML templates
│   └── templates/                # Template files
│
├── routes/                        # API routes
│   ├── auth.py
│   ├── attendance.py
│   ├── students.py
│   └── ...
│
├── venv/                          # Python virtual environment
│
└── Deployment Scripts:
    ├── production_deploy.sh       # Main deployment
    ├── setup_nginx.sh            # Nginx setup
    ├── setup_ssl.sh              # SSL certificate
    ├── backup_database.sh        # Database backup
    ├── check_health.sh           # Health monitoring
    └── gunicorn_production.conf.py
```

---

## 🔧 System Services Created

### Systemd Service
- **Name**: `madrasha.service`
- **Location**: `/etc/systemd/system/madrasha.service`
- **Purpose**: Auto-start application on boot, manage lifecycle
- **Commands**:
  ```bash
  sudo systemctl start madrasha
  sudo systemctl stop madrasha
  sudo systemctl restart madrasha
  sudo systemctl status madrasha
  sudo journalctl -u madrasha -f
  ```

### Nginx Configuration
- **Name**: `madrasha`
- **Location**: `/etc/nginx/sites-available/madrasha`
- **Enabled**: `/etc/nginx/sites-enabled/madrasha`
- **Purpose**: Reverse proxy, static file serving, HTTPS
- **Commands**:
  ```bash
  sudo nginx -t                    # Test configuration
  sudo systemctl restart nginx
  sudo tail -f /var/log/nginx/madrasha_error.log
  ```

---

## 🔐 Security Features

✅ **HTTPS/SSL** - Let's Encrypt certificate with auto-renewal
✅ **Secure Headers** - X-Frame-Options, X-Content-Type-Options, etc.
✅ **File Permissions** - Proper ownership (www-data) and restrictive permissions
✅ **Environment Variables** - Secrets stored in .env file (chmod 600)
✅ **Database Security** - SQLite file with restricted permissions
✅ **Service Isolation** - Application runs as www-data user
✅ **Firewall Ready** - Instructions for UFW firewall setup

---

## 💾 Backup Strategy

### Automated Daily Backups
- **Schedule**: Every day at 2:00 AM
- **Location**: `/var/www/madrasha/backups/`
- **Format**: `madrasha_backup_YYYYMMDD_HHMMSS.db.gz` (compressed)
- **Retention**: 30 days (automatic cleanup)
- **Manual Backup**: `sudo bash /var/www/madrasha/backup_database.sh`

### Restore from Backup
```bash
# Stop service
sudo systemctl stop madrasha

# Restore database (replace TIMESTAMP)
cd /var/www/madrasha
gunzip -c backups/madrasha_backup_TIMESTAMP.db.gz > instance/madrasha.db

# Fix permissions
sudo chown www-data:www-data instance/madrasha.db

# Start service
sudo systemctl start madrasha
```

---

## 📊 Monitoring & Health Checks

### Automatic Health Monitoring
- **Script**: `check_health.sh`
- **Schedule**: Every 5 minutes (via cron)
- **Checks**:
  - Service status (systemd)
  - HTTP endpoint health
  - Database file existence
  - Disk space usage
- **Auto-recovery**: Restarts service if unhealthy

### Manual Health Check
```bash
# Check service
sudo systemctl status madrasha

# Check application endpoint
curl http://localhost:5000/health

# Check logs
sudo journalctl -u madrasha -n 50
sudo tail -50 /var/www/madrasha/logs/gunicorn_error.log
```

---

## 🌐 Access Points

### After Deployment:

- **Public URL**: https://madrasaummulqura.com
- **Admin Panel**: https://madrasaummulqura.com (login page)
- **Health Endpoint**: https://madrasaummulqura.com/health

### Default Credentials:
| Role | Phone | Password |
|------|-------|----------|
| Super Admin | 01712345678 | admin123 |
| Teacher | 01812345678 | teacher123 |
| Junior Ustad | 01700000001 | junior123 |
| Student | 01912345678 | student123 |

**⚠️ Change all passwords immediately after first login!**

---

## 🔄 Update Procedure

### Deploying Updates:
```bash
# 1. Backup database
cd /var/www/madrasha
sudo bash backup_database.sh

# 2. Pull latest code
sudo git pull origin main

# 3. Update dependencies (if needed)
source venv/bin/activate
pip install -r requirements.txt

# 4. Restart service
sudo systemctl restart madrasha

# 5. Verify
sudo systemctl status madrasha
curl https://madrasaummulqura.com/health
```

---

## 📞 Troubleshooting Quick Reference

### Service Won't Start
```bash
sudo journalctl -u madrasha -n 100 --no-pager
sudo tail -50 /var/www/madrasha/logs/gunicorn_error.log
```

### Database Issues
```bash
ls -la /var/www/madrasha/instance/
sudo chown -R www-data:www-data /var/www/madrasha/instance
sudo chmod 664 /var/www/madrasha/instance/madrasha.db
```

### Nginx 502 Error
```bash
sudo systemctl status madrasha
sudo netstat -tlnp | grep 5000
sudo systemctl restart madrasha nginx
```

### SSL Certificate Issues
```bash
sudo certbot renew
sudo certbot renew --dry-run
sudo systemctl reload nginx
```

---

## 📝 Required Environment Variables

The `.env` file is auto-created during deployment with these defaults:

```env
FLASK_ENV=production
SECRET_KEY=<auto-generated>
DATABASE_URL=sqlite:///instance/madrasha.db

# Update these with your actual credentials:
SMS_API_KEY=your_sms_api_key_here
SMS_API_URL=your_sms_api_url_here
SMS_SENDER_ID=MadrasaUQ

APP_NAME=Madrasha Ummul Qura
DOMAIN=madrasaummulqura.com
```

**Edit after deployment**: `sudo nano /var/www/madrasha/.env`

---

## ✅ Deployment Verification

After deployment, verify:

1. ✅ Service is running: `sudo systemctl status madrasha`
2. ✅ Nginx is running: `sudo systemctl status nginx`
3. ✅ Database exists: `ls -lh /var/www/madrasha/instance/madrasha.db`
4. ✅ Site is accessible: Open https://madrasaummulqura.com
5. ✅ SSL is working: Check for green padlock in browser
6. ✅ Login works: Test with admin credentials
7. ✅ Backups are configured: `sudo crontab -l`

---

## 📚 Documentation Files

- **`QUICK_START.md`** - Fast deployment commands
- **`DEPLOYMENT_CHECKLIST.md`** - Step-by-step checklist
- **`VPS_DEPLOYMENT_GUIDE.md`** - Complete deployment guide
- **`PRODUCTION_SUMMARY.md`** - This file

---

## 🎉 You're Ready!

Everything is configured and ready for production deployment. Just:

1. Push these changes to GitHub
2. Pull on your VPS
3. Run the deployment scripts
4. Access your site at https://madrasaummulqura.com

**Need help?** Check the deployment guide or checklist for detailed instructions.

---

**Deployed By**: Your Team
**Date**: October 24, 2025
**Status**: ✅ Production Ready
