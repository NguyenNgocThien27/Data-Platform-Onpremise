FROM postgres:9.5.3

COPY hive-db-init.sh /docker-entrypoint-initdb.d/hive-db-init.sh

RUN chmod +x /docker-entrypoint-initdb.d/hive-db-init.sh

EXPOSE 5432