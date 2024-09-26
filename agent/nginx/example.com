server {
    listen 80;  # Lắng nghe trên cổng 80
    server_name example.com;  # Tên miền của bạn

    root /var/www/html;  # Đường dẫn đến thư mục gốc
    index index.html index.htm index.php;

    # Ghi log truy cập
    access_log /var/log/nginx/access.log custom;  # Thay đổi đường dẫn nếu cần

    location / {
        try_files $uri $uri/ =404;  # Kiểm tra xem file có tồn tại không
    }

    # Các khối xử lý khác...
}
