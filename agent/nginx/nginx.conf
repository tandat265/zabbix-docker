# Định nghĩa người dùng và số lượng quy trình worker
user www-data;
worker_processes auto;

# Thiết lập mức độ ghi log lỗi
error_log /var/log/nginx/error.log;
pid /var/run/nginx.pid;

# Định nghĩa sự kiện
events {
    worker_connections 1024;
}

# Khối HTTP
http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Định dạng log tùy chỉnh bao gồm URL đã nhập
    log_format custom '$remote_addr - $remote_user [$time_local] "$request" '
                     '$status $body_bytes_sent "$http_referer" '
                     '"$http_user_agent" "$http_x_forwarded_for" "$request_uri"';

    # Thiết lập file ghi log truy cập với định dạng tùy chỉnh
    access_log /var/log/nginx/access.log custom;

    # Thiết lập sendfile để chuyển file hiệu quả
    sendfile on;

    # Thiết lập keep-alive
    keepalive_timeout 65;

    # Thiết lập Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Khối server
    server {
        listen 80;  # Lắng nghe trên cổng 80
        server_name example.com;  # Tên miền của bạn

        # Thư mục gốc
        root /var/www/html;  # Thay đổi theo đường dẫn của tài liệu gốc
        index index.html index.htm index.php;

        # Xử lý yêu cầu GET và POST
        location / {
            try_files $uri $uri/ =404;  # Kiểm tra xem file có tồn tại không
        }

        # Xử lý PHP nếu cần
        location ~ \.php$ {
            include snippets/fastcgi-php.conf;
            fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;  # Thay đổi theo phiên bản PHP của bạn
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include fastcgi_params;
        }

        # Xử lý yêu cầu không tìm thấy
        error_page 404 /404.html;
        location = /404.html {
            root /var/www/html;
        }

        # Xử lý lỗi server
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root /var/www/html;
        }
    }
}
