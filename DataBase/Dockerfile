FROM mysql:8.0

ENV MYSQL_DATABASE=notibolt
ENV MYSQL_ROOT_PASSWORD=root_password

COPY ./create_db.sql /docker-entrypoint-initdb.d/

EXPOSE 3306