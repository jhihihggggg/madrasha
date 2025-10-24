#!/bin/bash
# Health Check Script for Madrasha Application
# Runs every 5 minutes via cron to ensure service is healthy
# Add to crontab: */5 * * * * /var/www/madrasha/check_health.sh >> /var/www/madrasha/logs/health_check.log 2>&1

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
APP_URL="http://localhost:8000/health"
SERVICE_NAME="madrasha"
ALERT_EMAIL="admin@madrasaummulqura.com"  # Change this

echo "[$TIMESTAMP] Running health check..."

# Check if service is running
if ! systemctl is-active --quiet $SERVICE_NAME; then
    echo "[$TIMESTAMP] ❌ Service is not running! Attempting restart..."
    systemctl restart $SERVICE_NAME
    sleep 5
    
    if systemctl is-active --quiet $SERVICE_NAME; then
        echo "[$TIMESTAMP] ✓ Service restarted successfully"
    else
        echo "[$TIMESTAMP] ❌ Failed to restart service!"
        # Send alert (requires mailutils to be installed)
        # echo "Madrasha service failed to restart at $TIMESTAMP" | mail -s "ALERT: Madrasha Service Down" $ALERT_EMAIL
    fi
else
    echo "[$TIMESTAMP] ✓ Service is running"
fi

# Check application health endpoint
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $APP_URL)

if [ "$HTTP_CODE" == "200" ]; then
    echo "[$TIMESTAMP] ✓ Application is healthy (HTTP $HTTP_CODE)"
else
    echo "[$TIMESTAMP] ⚠️  Application returned HTTP $HTTP_CODE"
    
    # Try to restart if unhealthy
    if [ "$HTTP_CODE" == "000" ] || [ "$HTTP_CODE" == "500" ] || [ "$HTTP_CODE" == "502" ]; then
        echo "[$TIMESTAMP] Restarting service due to unhealthy status..."
        systemctl restart $SERVICE_NAME
    fi
fi

# Check disk space
DISK_USAGE=$(df -h /var/www/madrasha | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    echo "[$TIMESTAMP] ⚠️  Disk usage is at ${DISK_USAGE}%"
fi

# Check database file
DB_FILE="/var/www/madrasha/instance/madrasha.db"
if [ ! -f "$DB_FILE" ]; then
    echo "[$TIMESTAMP] ❌ Database file not found!"
else
    DB_SIZE=$(du -h "$DB_FILE" | cut -f1)
    echo "[$TIMESTAMP] ✓ Database file exists (Size: $DB_SIZE)"
fi

echo "[$TIMESTAMP] Health check complete"
echo "---"
