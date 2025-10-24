# 🚀 VPS Production Deployment - Start Here!

## madrasaummulqura.com - Quick Deployment

### On Your Ubuntu VPS (as root):

```bash
# 1. Clone repository
cd /var/www
git clone https://github.com/jhihihggggg/madrasha.git
cd madrasha

# 2. Make scripts executable  
chmod +x *.sh

# 3. Deploy (takes 5-10 minutes)
bash production_deploy.sh

# 4. Setup Nginx
bash setup_nginx.sh

# 5. Setup SSL (after DNS points to VPS)
bash setup_ssl.sh
```

## ✅ That's It!

Your site will be live at: **https://madrasaummulqura.com**

---

## 📚 Full Documentation

- **Quick Start**: [`QUICK_START.md`](QUICK_START.md)
- **Deployment Checklist**: [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md)
- **Complete Guide**: [`VPS_DEPLOYMENT_GUIDE.md`](VPS_DEPLOYMENT_GUIDE.md)
- **Summary**: [`PRODUCTION_SUMMARY.md`](PRODUCTION_SUMMARY.md)

---

## 🔧 After Deployment

**✅ SMS is already configured!** No need to edit anything for SMS.

The application uses hardcoded BulkSMSBD API credentials. SMS will work immediately after deployment.

```bash
# Only if you want to change SECRET_KEY or other settings
nano /var/www/madrasha/.env

# Restart application
systemctl restart madrasha
```

See [SMS_CONFIGURATION.md](SMS_CONFIGURATION.md) for details.

---

## 🔐 Default Login

- **Phone**: 01712345678
- **Password**: admin123

*Change password after first login!*

---

## 📊 Useful Commands

```bash
# Service management
systemctl status madrasha
systemctl restart madrasha
journalctl -u madrasha -f

# View logs
tail -f /var/www/madrasha/logs/gunicorn_error.log
tail -f /var/log/nginx/madrasha_error.log

# Backup database
bash /var/www/madrasha/backup_database.sh

# Update application
cd /var/www/madrasha
git pull
systemctl restart madrasha
```

---

## ⚡ Need Help?

Check [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md) for the complete step-by-step guide with troubleshooting.
