FROM mysql:latest

# RUN wget http://security.ubuntu.com/ubuntu/pool/main/a/apt/apt_1.0.1ubuntu2.17_amd64.deb -O apt.deb
# RUN dpkg -i apt.deb

# # Install dependencies & JAVA
# RUN apt-get update -yqq && \
#     apt-get upgrade -yqq && \
#     apt-get install -yqq --no-install-recommends \
#     apt-utils \
#     curl \
#     openjdk-8-jdk \
#     wget \
#     netcat && \
#     apt-get autoremove -yqq --purge \
#     vim \
#     nano

RUN chmod -R 775 /docker-entrypoint-initdb.d

RUN echo "CREATE USER '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';" > /docker-entrypoint-initdb.d/create-user.sql \
    && echo "CREATE DATABASE ${MYSQL_DATABASE};" >> /docker-entrypoint-initdb.d/create-user.sql \
    && echo "GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'%';" >> /docker-entrypoint-initdb.d/create-user.sql \
    && echo "GRANT RELOAD ON *.* TO 'mysqluser'@'%';" >> /docker-entrypoint-initdb.d/create-user.sql\
    && echo "create table inventory.customers (id int, name varchar(30));" >> /docker-entrypoint-initdb.d/create-user.sql\
    && echo "GRANT REPLICATION CLIENT ON *.* TO 'mysqluser'@'%';" >> /docker-entrypoint-initdb.d/create-user.sql\
    && echo "GRANT REPLICATION SLAVE ON *.* TO 'mysqluser'@'%';" >> /docker-entrypoint-initdb.d/create-user.sql\
    && echo "FLUSH PRIVILEGES;" >> /docker-entrypoint-initdb.d/create-user.sql
