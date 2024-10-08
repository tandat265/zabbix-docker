#!/bin/sh
service nginx start
service elasticsearch start
service ssh start
service zabbix-agent start
service rsyslog start
filebeat -e -c /etc/filebeat/filebeat.yml
chown -R www-data:www-data /var/log/nginx/ 
touch /var/log/auth.log
chmod 644 /var/log/auth.log
chown syslog:adm /var/log/auth.log
chmod 644 /var/log/nginx/access.log
chmod 644 /var/log/nginx/error.log
python3.10 /ai/kafka_consumer.py
