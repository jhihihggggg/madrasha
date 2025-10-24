#!/bin/bash
# Database Backup Script for Madrasha Ummul Qura
# Add to crontab for automatic daily backups:
# 0 2 * * * /var/www/madrasha/backup_database.sh

set -e

echo "💾 Backing up Madrasha database..."

# Configuration
PROJECT_DIR="/var/www/madrasha"
DB_FILE="$PROJECT_DIR/instance/madrasha.db"
BACKUP_DIR="$PROJECT_DIR/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/madrasha_backup_$TIMESTAMP.db"

# Retention (keep backups for 30 days)
RETENTION_DAYS=30

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Check if database exists
if [ ! -f "$DB_FILE" ]; then
    echo "❌ Database file not found: $DB_FILE"
    exit 1
fi

# Create backup
echo "Creating backup: $BACKUP_FILE"
sqlite3 $DB_FILE ".backup $BACKUP_FILE"

# Compress the backup
echo "Compressing backup..."
gzip $BACKUP_FILE

# Verify backup
if [ -f "${BACKUP_FILE}.gz" ]; then
    SIZE=$(du -h "${BACKUP_FILE}.gz" | cut -f1)
    echo "✓ Backup created successfully: ${BACKUP_FILE}.gz (${SIZE})"
else
    echo "❌ Backup failed!"
    exit 1
fi

# Delete old backups
echo "Cleaning up old backups (older than $RETENTION_DAYS days)..."
find $BACKUP_DIR -name "madrasha_backup_*.db.gz" -type f -mtime +$RETENTION_DAYS -delete
echo "✓ Cleanup complete"

# List recent backups
echo ""
echo "Recent backups:"
ls -lh $BACKUP_DIR/madrasha_backup_*.db.gz | tail -5

echo ""
echo "✅ Backup complete!"
