# 📋 VPS Production Deployment Checklist

## Pre-Deployment Checklist

### VPS Setup
- [ ] Ubuntu 20.04/22.04 VPS with root access
- [ ] Minimum 2GB RAM, 20GB disk space
- [ ] VPS IP address noted: `________________`
- [ ] SSH access working

### Domain Setup  
- [ ] Domain registered: `madrasaummulqura.com`
- [ ] DNS A record created pointing to VPS IP
- [ ] DNS propagation complete (test with `dig madrasaummulqura.com`)
- [ ] Optional: `www.madrasaummulqura.com` A record created

### Required Accounts
- [ ] GitHub account with repository access
- [ ] SMS API provider account (for notifications)
- [ ] Email for SSL certificate notifications

---

## Deployment Steps

### 1. Server Preparation
```bash
# Update system
- [ ] sudo apt update && sudo apt upgrade -y

# Install dependencies  
- [ ] sudo apt install -y python3 python3-pip python3-venv git nginx sqlite3 certbot python3-certbot-nginx

# Verify installations
- [ ] python3 --version  # Should be 3.8+
- [ ] nginx -v
- [ ] git --version
```

### 2. Clone Repository
```bash
- [ ] cd /var/www
- [ ] sudo git clone https://github.com/jhihihggggg/madrasha.git
- [ ] cd madrasha
- [ ] ls -la  # Verify files are there
```

### 3. Make Scripts Executable
```bash
- [ ] sudo chmod +x production_deploy.sh
- [ ] sudo chmod +x setup_nginx.sh
- [ ] sudo chmod +x setup_ssl.sh
- [ ] sudo chmod +x backup_database.sh
- [ ] ls -l *.sh  # Verify permissions (should see -rwxr-xr-x)
```

### 4. Run Main Deployment
```bash
- [ ] sudo bash production_deploy.sh
- [ ] Wait for completion (may take 5-10 minutes)
- [ ] Check for any errors in output
- [ ] Verify service is running: sudo systemctl status madrasha
```

### 5. Configure Environment Variables
```bash
- [ ] sudo nano /var/www/madrasha/.env
- [ ] Update SMS_API_KEY with actual key
- [ ] Update SMS_API_URL with actual URL
- [ ] Update SMS_SENDER_ID if needed
- [ ] Save and exit (Ctrl+X, Y, Enter)
- [ ] sudo systemctl restart madrasha
```

### 6. Setup Nginx Reverse Proxy
```bash
- [ ] sudo bash setup_nginx.sh
- [ ] Verify Nginx is running: sudo systemctl status nginx
- [ ] Test config: sudo nginx -t
- [ ] Test HTTP access: curl http://madrasaummulqura.com
```

### 7. Setup SSL Certificate
```bash
# ONLY after DNS is pointing to your VPS!
- [ ] Verify DNS: dig madrasaummulqura.com
- [ ] sudo bash setup_ssl.sh
- [ ] Follow prompts and enter email
- [ ] Test HTTPS: curl https://madrasaummulqura.com
- [ ] Open in browser: https://madrasaummulqura.com
```

### 8. Setup Automatic Backups
```bash
- [ ] sudo crontab -e
- [ ] Add line: 0 2 * * * /var/www/madrasha/backup_database.sh >> /var/www/madrasha/logs/backup.log 2>&1
- [ ] Save and exit
- [ ] Verify cron: sudo crontab -l
- [ ] Test manually: sudo bash /var/www/madrasha/backup_database.sh
```

---

## Post-Deployment Verification

### Application Testing
- [ ] Open https://madrasaummulqura.com in browser
- [ ] Page loads without errors
- [ ] Login page displays correctly
- [ ] Test super admin login (01712345678 / admin123)
- [ ] Dashboard loads successfully
- [ ] Test attendance marking
- [ ] Test student list display
- [ ] Test batch management

### Security Configuration
- [ ] Change default admin password immediately
- [ ] Change all default user passwords
- [ ] Verify .env file permissions: ls -l /var/www/madrasha/.env (should be -rw-------)
- [ ] Setup firewall:
  ```bash
  - [ ] sudo ufw allow OpenSSH
  - [ ] sudo ufw allow 'Nginx Full'
  - [ ] sudo ufw enable
  - [ ] sudo ufw status
  ```

### Service Health Checks
```bash
- [ ] sudo systemctl status madrasha  # Should be "active (running)"
- [ ] sudo systemctl status nginx     # Should be "active (running)"
- [ ] curl http://localhost:5000/health  # Should return {"status":"healthy"}
- [ ] ps aux | grep gunicorn  # Should show running workers
```

### Log Verification
```bash
- [ ] sudo journalctl -u madrasha -n 20  # Check for errors
- [ ] sudo tail -20 /var/log/nginx/madrasha_access.log
- [ ] sudo tail -20 /var/log/nginx/madrasha_error.log
- [ ] sudo tail -20 /var/www/madrasha/logs/gunicorn_error.log
```

### Database Verification
```bash
- [ ] ls -lh /var/www/madrasha/instance/madrasha.db  # Should exist
- [ ] file /var/www/madrasha/instance/madrasha.db  # Should say "SQLite 3.x database"
- [ ] sqlite3 /var/www/madrasha/instance/madrasha.db "SELECT COUNT(*) FROM users;"  # Should show count > 0
```

---

## Performance Optimization

### Optional: Enable Gzip Compression
```bash
- [ ] sudo nano /etc/nginx/nginx.conf
- [ ] Uncomment/add gzip settings in http block:
      gzip on;
      gzip_vary on;
      gzip_proxied any;
      gzip_comp_level 6;
      gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;
- [ ] sudo nginx -t
- [ ] sudo systemctl reload nginx
```

### Optional: Setup Fail2Ban (SSH Protection)
```bash
- [ ] sudo apt install -y fail2ban
- [ ] sudo systemctl enable fail2ban
- [ ] sudo systemctl start fail2ban
- [ ] sudo fail2ban-client status
```

---

## Monitoring Setup

### Create Monitoring Script
```bash
- [ ] Create /var/www/madrasha/check_health.sh
- [ ] Add to crontab: */5 * * * * /var/www/madrasha/check_health.sh
- [ ] Test: sudo bash /var/www/madrasha/check_health.sh
```

### Setup Log Rotation
```bash
- [ ] Create /etc/logrotate.d/madrasha
- [ ] Add configuration for application logs
- [ ] Test: sudo logrotate -d /etc/logrotate.d/madrasha
```

---

## Documentation

- [ ] Document VPS IP address
- [ ] Document admin credentials (store securely!)
- [ ] Document SMS API credentials
- [ ] Document SSL certificate renewal date
- [ ] Create backup restoration procedure document
- [ ] Document custom configurations made

---

## Final Checks

### Functionality Testing
- [ ] Super Admin can login
- [ ] Teacher can login  
- [ ] Junior Ustad can login
- [ ] Student can login
- [ ] Attendance can be marked
- [ ] SMS notifications work (if configured)
- [ ] File uploads work
- [ ] Batch management works
- [ ] Student records display correctly

### Browser Testing
- [ ] Test in Chrome/Chromium
- [ ] Test in Firefox
- [ ] Test in Safari (if available)
- [ ] Test on mobile browser
- [ ] Test HTTPS lock icon appears
- [ ] No mixed content warnings

### Performance Testing
```bash
- [ ] Page load time < 3 seconds
- [ ] Database queries respond quickly
- [ ] No timeout errors
- [ ] Application responsive under load
```

---

## Emergency Contacts & Info

**VPS Provider**: ___________________
**VPS IP**: ___________________
**Domain Registrar**: ___________________
**SSH Port**: ___________________
**Admin Email**: ___________________
**SMS Provider**: ___________________

---

## Rollback Plan (If Needed)

If deployment fails:

1. **Stop service**: `sudo systemctl stop madrasha`
2. **Restore backup**: 
   ```bash
   cd /var/www/madrasha
   gunzip -c backups/madrasha_backup_TIMESTAMP.db.gz > instance/madrasha.db
   ```
3. **Revert code**: `sudo git reset --hard HEAD~1`
4. **Restart**: `sudo systemctl start madrasha`

---

## Support Resources

- [ ] Full deployment guide reviewed: `VPS_DEPLOYMENT_GUIDE.md`
- [ ] Quick start guide available: `QUICK_START.md`
- [ ] Troubleshooting section bookmarked
- [ ] Backup scripts tested
- [ ] Recovery procedure documented

---

## Sign-Off

**Deployed By**: ___________________
**Date**: ___________________
**VPS IP**: ___________________
**Domain**: madrasaummulqura.com
**Status**: ⬜ Deployed ⬜ Verified ⬜ Production-Ready

**Notes**:
_____________________________________________
_____________________________________________
_____________________________________________

---

## ✅ DEPLOYMENT COMPLETE!

Congratulations! Your Madrasha management system is now live at:
**https://madrasaummulqura.com** 🎉
