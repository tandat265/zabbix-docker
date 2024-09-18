# Bắt đầu từ hình ảnh Ubuntu chính thức
FROM ubuntu:20.04

# Thiết lập biến môi trường để không bị hỏi khi cài đặt
ENV DEBIAN_FRONTEND=noninteractive
# Thiết lập biến môi trường cho MySQL root user
ENV MYSQL_ROOT_PASSWORD=root

# Cập nhật hệ thống và cài đặt các gói cần thiết
RUN apt-get update && \
    apt-get install -y \
    wget \
    curl \
    lsb-release \
    locales

# Cài đặt MariaDB (hoặc MySQL)
RUN apt-get install -y mariadb-server mariadb-client

# Thêm kho lưu trữ Zabbix
RUN wget https://repo.zabbix.com/zabbix/6.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.0-1+ubuntu20.04_all.deb && \
    dpkg -i zabbix-release_6.0-1+ubuntu20.04_all.deb && \
    apt-get update

# Cài đặt Zabbix Server và các thành phần liên quan
RUN apt-get install -y \
    zabbix-server-mysql \
    zabbix-agent \
    php-mysql \
    zabbix-sql-scripts \
    zabbix-apache-conf \
    zabbix-frontend-php && \
    apt-get -f install -y
    
# Cấu hình locale
RUN sed -i '/^# en_US.UTF-8/s/^# //' /etc/locale.gen && \
    locale-gen
    
# Thiết lập biến môi trường locale
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8


# Tạo thư mục docker-entrypoint-initdb.d nếu chưa tồn tại
RUN mkdir -p /docker-entrypoint-initdb.d/

# Sao chép tệp server.sql.gz từ gói Zabbix đã cài đặt vào docker-entrypoint-initdb.d
RUN cp /usr/share/zabbix-sql-scripts/mysql/server.sql.gz /docker-entrypoint-initdb.d/

# Copy file cấu hình của Zabbix Server và các tệp khởi tạo
COPY ./zabbix/zabbix_server.conf /etc/zabbix/zabbix_server.conf
COPY ./zabbix/apache.conf /etc/zabbix/apache.conf
COPY ./mysql/init-db.sql /docker-entrypoint-initdb.d/
COPY ./mysql/import-schema.sh /docker-entrypoint-initdb.d/

# Thiết lập quyền thực thi cho script import
RUN chmod +x /docker-entrypoint-initdb.d/import-schema.sh

# Expose các cổng cần thiết
EXPOSE 3306 10051 80

# Script khởi chạy dịch vụ
CMD ["sh", "-c", "service mysql start && sleep 10 && mysql < /docker-entrypoint-initdb.d/init-db.sql && /docker-entrypoint-initdb.d/import-schema.sh && service apache2 start && /usr/sbin/zabbix_server && tail -f /dev/null"]

