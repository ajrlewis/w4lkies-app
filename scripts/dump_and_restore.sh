#! /bin/bash

source .env

backupfile="backups/w4lkies_db $(date +'%Y-%m-%d').bak"

echo $backupfile

# Dump from remote
pg_dump -Fc -v -d "postgresql://${remote_user}:${remote_password}@${remote_hostname}/${remote_dbname}?sslmode=require" -f "${backupfile}"

# Restore to local
pg_restore -v -c -d postgresql://${local_user}:${local_password}@${local_hostname}/${local_dbname} "${backupfile}"
