/bin/bash
psql -U username -d database -f /docker-entrypoint-initdb.d/generate_tables.sql