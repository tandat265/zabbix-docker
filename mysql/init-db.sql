-- Tạo cơ sở dữ liệu Zabbix nếu chưa tồn tại
CREATE DATABASE IF NOT EXISTS zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

-- Tạo người dùng Zabbix nếu chưa tồn tại
CREATE USER IF NOT EXISTS 'zabbix'@'localhost' IDENTIFIED BY 'zabbix';

-- Gán quyền cho người dùng Zabbix
GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'localhost';

-- Áp dụng quyền
FLUSH PRIVILEGES;
