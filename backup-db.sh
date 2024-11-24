BACKUP_DIR="/backup/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/backup_${TIMESTAMP}.sql"

# Create backup directory if it doesn't exist
mkdir -p ${BACKUP_DIR}

# Backup database
docker exec fastapi-app_db_1 pg_dump -U postgres mindsync > ${BACKUP_FILE}

# Compress backup
gzip ${BACKUP_FILE}

# Keep only last 7 days of backups
find ${BACKUP_DIR} -type f -mtime +7 -delete