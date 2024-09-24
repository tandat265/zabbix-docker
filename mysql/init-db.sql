-- Tạo cơ sở dữ liệu Zabbix nếu chưa tồn tại
CREATE DATABASE IF NOT EXISTS zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

-- Tạo người dùng Zabbix nếu chưa tồn tại
CREATE USER IF NOT EXISTS 'zabbix'@'localhost' IDENTIFIED BY 'zabbix';

-- Gán quyền cho người dùng Zabbix
GRANT SUPER ON *.* TO 'zabbix'@'localhost';

-- Áp dụng quyền
FLUSH PRIVILEGES;

SET GLOBAL log_bin_trust_function_creators = 1;
