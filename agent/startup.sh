service nginx start
service elasticsearch start
service zabbix-agent start
filebeat -e -c /etc/filebeat/filebeat.yml
python3.10 /ai/kafka_consumer.py
chown -R www-data:www-data /var/log/nginx/ 
chmod 644 /var/log/nginx/access.log
chmod 644 /var/log/nginx/error.log
