# 🚀 Quick Start - VPS Deployment for madrasaummulqura.com

## One-Command Deployment

### On Your Ubuntu VPS:

```bash
# 1. Clone repository
cd /var/www
sudo git clone https://github.com/jhihihggggg/madrasha.git
cd madrasha

# 2. Make scripts executable
sudo chmod +x *.sh

# 3. Run deployment
sudo bash production_deploy.sh

# 4. Setup Nginx
sudo bash setup_nginx.sh

# 5. Setup SSL (after DNS is pointing to your VPS)
sudo bash setup_ssl.sh
```

## What Gets Deployed:

✅ Flask application with Gunicorn WSGI server
✅ SQLite database in `/var/www/madrasha/instance/`
✅ Systemd service for auto-start
✅ Nginx reverse proxy
✅ SSL certificate (HTTPS)
✅ Automatic daily backups
✅ **SMS already configured (BulkSMSBD API hardcoded)**

## Access Your Site:

- **URL**: https://madrasaummulqura.com
- **Admin Login**: 01712345678 / admin123
- **SMS**: Already working! No configuration needed.

## Useful Commands:

```bash
# Service management
sudo systemctl restart madrasha
sudo systemctl status madrasha
sudo journalctl -u madrasha -f

# View logs
sudo tail -f /var/www/madrasha/logs/gunicorn_error.log

# Backup database
sudo bash /var/www/madrasha/backup_database.sh

# Update application
cd /var/www/madrasha
sudo git pull
sudo systemctl restart madrasha
```

## Troubleshooting:

If something doesn't work:

1. Check service status:
   ```bash
   sudo systemctl status madrasha
   sudo systemctl status nginx
   ```

2. View error logs:
   ```bash
   sudo journalctl -u madrasha -n 100
   sudo tail -50 /var/log/nginx/madrasha_error.log
   ```

3. Verify permissions:
   ```bash
   ls -la /var/www/madrasha/instance/
   ```

## Files Created:

- `/var/www/madrasha/` - Application directory
- `/var/www/madrasha/instance/madrasha.db` - SQLite database
- `/var/www/madrasha/backups/` - Database backups
- `/etc/systemd/system/madrasha.service` - Systemd service
- `/etc/nginx/sites-available/madrasha` - Nginx config

## Need Help?

Check the full guide: `VPS_DEPLOYMENT_GUIDE.md`
