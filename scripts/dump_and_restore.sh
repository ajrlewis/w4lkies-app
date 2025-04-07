#! /bin/bash

source .env

backupfile="backups/w4lkies_db $(date +'%Y-%m-%d').sql"
echo $backupfile

# Dump from remote
pg_dump -F p -v --clean -d "postgresql://${remote_user}:${remote_password}@${remote_hostname}/${remote_dbname}?sslmode=require" -f "${backupfile}"

# Restore to local
psql -v --clean -d "postgresql://${local_user}:${local_password}@${local_hostname}/${local_dbname}" -f "${backupfile}"
