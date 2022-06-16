FROM postgres:12.7
ENV POSTGRES_PASSWORD=secret
ENV POSTGRES_USER=username
ENV POSTGRES_DB=database
COPY database/generate_tables.sql /docker-entrypoint-initdb.d/generate_tables.sql
COPY database/entrypoint.sh /docker-entrypoint-initdb.d/entrypoint.sh
RUN ["chmod", "+x", "/docker-entrypoint-initdb.d/entrypoint.sh"]