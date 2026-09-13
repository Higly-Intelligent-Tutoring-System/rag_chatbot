#!/usr/bin/env bash

set -Eeuo pipefail
umask 077

: "${PGHOST:=db}"
: "${PGPORT:=5432}"
: "${PGUSER:?PGUSER is required}"
: "${PGPASSWORD:?PGPASSWORD is required}"
: "${DATABASES:?DATABASES is required}"
: "${AGE_RECIPIENT:?AGE_RECIPIENT is required}"
: "${RCLONE_DEST:?RCLONE_DEST is required}"

BACKUP_PREFIX="${BACKUP_PREFIX:-postgres}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

export PGHOST PGPORT PGUSER PGPASSWORD

WORKDIR="$(mktemp -d)"

cleanup() {
    rm -rf "$WORKDIR"
}

trap cleanup EXIT

timestamp="$(date -u '+%Y-%m-%dT%H-%M-%SZ')"
backup_dir="${BACKUP_PREFIX}-${timestamp}"
backup_path="$WORKDIR/$backup_dir"

mkdir -p "$backup_path"

echo "Testing PostgreSQL connection..."

psql \
    -X \
    -v ON_ERROR_STOP=1 \
    --dbname=postgres \
    --command="SELECT 1;" \
    >/dev/null

echo "Backing up global PostgreSQL objects..."

pg_dumpall \
    --globals-only \
    --no-role-passwords \
| gzip \
| age \
    --recipient "$AGE_RECIPIENT" \
    --output "$backup_path/globals.sql.gz.age"

for database in $DATABASES; do
    safe_database="$(printf '%s' "$database" | sed 's/[^A-Za-z0-9_.-]/_/g')"
    output="$backup_path/${safe_database}.sql.gz.age"

    echo "Backing up database: $database"

    pg_dump \
        --dbname="$database" \
        --format=plain \
    | gzip \
    | age \
        --recipient "$AGE_RECIPIENT" \
        --output "$output"
done

echo "Uploading backup to $RCLONE_DEST/$backup_dir..."

rclone copy \
    "$backup_path" \
    "$RCLONE_DEST/$backup_dir"

echo "Backup uploaded successfully."

if [ "$RETENTION_DAYS" -gt 0 ]; then
    echo "Deleting files older than $RETENTION_DAYS days..."

    rclone delete \
        "$RCLONE_DEST" \
        --min-age "${RETENTION_DAYS}d" \
        --include "${BACKUP_PREFIX}-*/**"
fi

echo "Backup completed: $backup_dir"