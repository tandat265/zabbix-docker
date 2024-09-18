#!/bin/bash
# Import Zabbix schema sau khi MySQL khởi động

# Kiểm tra nếu file schema tồn tại và giải nén, sau đó import
if [ -f /docker-entrypoint-initdb.d/server.sql.gz ]; then
    echo "Importing Zabbix database schema..."
    zcat /docker-entrypoint-initdb.d/server.sql.gz | mysql -uzabbix -pzabbix zabbix
fi

