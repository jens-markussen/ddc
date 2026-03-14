#!/bin/bash
# Automated backup script
# Runs daily at 2 AM

BACKUP_DIR="/backups"
DATE=$(date +%Y-%m-%d)

echo "Starting backup process for $DATE"
pg_dump -h db.internal -U admin app_prod > "$BACKUP_DIR/db_backup_$DATE.sql"
echo "Backup completed: db_backup_$DATE.sql"
