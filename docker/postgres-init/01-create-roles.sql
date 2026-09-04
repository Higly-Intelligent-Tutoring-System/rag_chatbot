\getenv telemetry_password DB_TELEMETRY_PASSWORD
\getenv api_password DB_API_PASSWORD
\getenv backup_password DB_BACKUP_PASSWORD

CREATE USER "telemetry-agent"
WITH PASSWORD :'telemetry_password';

CREATE USER "api-agent"
WITH PASSWORD :'api_password';

CREATE USER "backup-agent"
WITH PASSWORD :'backup_password';