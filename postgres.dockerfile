FROM postgres
COPY ./db_dumps/jspanda_pg_dump.sql /docker-entrypoint-initdb.d/jspanda_pg_dump.sql