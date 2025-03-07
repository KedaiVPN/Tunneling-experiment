#!/bin/bash

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Update package lists
apt-get update

# Install Nginx
apt-get install -y nginx

# Backup original nginx.conf
mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# Create new nginx.conf
cat > /etc/nginx/nginx.conf <<'EOL'
user www-data;
worker_processes auto;
worker_rlimit_nofile 65536;  # Meningkatkan batas file deskriptor
pid /var/run/nginx.pid;

events {
    multi_accept on;
    worker_connections 2048;  # Meningkatkan jumlah koneksi worker
}

http {
    gzip on;
    gzip_vary on;
    gzip_comp_level 5;
    gzip_types text/plain application/x-javascript text/xml text/css;
    autoindex on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    client_max_body_size 32M;
    client_header_buffer_size 8m;
    large_client_header_buffers 8 8m;
    fastcgi_buffer_size 8m;
    fastcgi_buffers 8 8m;
    fastcgi_read_timeout 600;

    #CloudFlare IPv4
    set_real_ip_from 199.27.128.0/21;
    set_real_ip_from 173.245.48.0/20;
    set_real_ip_from 103.21.244.0/22;
    set_real_ip_from 103.22.200.0/22;
    set_real_ip_from 103.31.4.0/22;
    set_real_ip_from 141.101.64.0/18;
    set_real_ip_from 108.162.192.0/18;
    set_real_ip_from 190.93.240.0/20;
    set_real_ip_from 188.114.96.0/20;
    set_real_ip_from 197.234.240.0/22;
    set_real_ip_from 198.41.128.0/17;
    set_real_ip_from 162.158.0.0/15;
    set_real_ip_from 104.16.0.0/12;

    #Incapsula
    set_real_ip_from 199.83.128.0/21;
    set_real_ip_from 198.143.32.0/19;
    set_real_ip_from 149.126.72.0/21;
    set_real_ip_from 103.28.248.0/22;
    set_real_ip_from 45.64.64.0/22;
    set_real_ip_from 185.11.124.0/22;
    set_real_ip_from 192.230.64.0/18;
    real_ip_header CF-Connecting-IP;

    include /etc/nginx/conf.d/*.conf;
}
EOL

# Create default server configuration
cat > /etc/nginx/conf.d/default.conf <<'EOL'
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:58080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws {
        proxy_pass http://127.0.0.1:1010;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOL

# Test nginx configuration
log "Testing Nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    # Restart Nginx
    systemctl restart nginx
    systemctl enable nginx
    log "Nginx configuration updated and service restarted"
    
    # Show status
    systemctl status nginx
else
    log "Error: Nginx configuration test failed"
    exit 1
fi

# Show completion message
clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "          NGINX SETUP COMPLETED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Configuration : /etc/nginx/nginx.conf"
echo "Default Site  : /etc/nginx/conf.d/default.conf"
echo "Access Log    : /var/log/nginx/access.log"
echo "Error Log     : /var/log/nginx/error.log"
echo ""
echo "Nginx service is running and enabled"
echo ""
echo "Press any key to continue..."
read -n 1 -s -r
clear
