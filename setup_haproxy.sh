#!/bin/bash

# Update package lists
apt-get update

# Install HAProxy
apt-get install -y haproxy

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to validate domain
validate_domain() {
    local domain="$1"
    if [[ ! "$domain" =~ ^[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
        return 1
    fi
    return 0
}

# Function to get domain input
get_domain() {
    clear
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "          DOMAIN INPUT SETUP"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Please input your domain"
    echo "Make sure your domain is already pointed to your IP"
    echo ""
    read -p "Enter domain : " domain

    # Validate domain format
    if ! validate_domain "$domain"; then
        echo ""
        echo "Invalid domain format. Please try again."
        echo "Press any key to continue..."
        read -n 1 -s -r
        get_domain
        return
    fi

    echo ""
    echo "Domain: $domain"
    echo ""
    read -p "Is this correct? [Y/n] " confirm

    if [[ "${confirm,,}" =~ ^(y|yes|)$ ]]; then
        # Create directory if it doesn't exist
        mkdir -p /etc/haproxy
        echo "$domain" > /etc/haproxy/domain.txt
        log "Domain saved: $domain"
        return 0
    else
        get_domain
    fi
}

# Create necessary directories
log "Creating necessary directories..."
mkdir -p /run/haproxy
mkdir -p /var/lib/haproxy

# Get domain input
get_domain
domain=$(cat /etc/haproxy/domain.txt)

# Generate self-signed certificate if not exists
if [ ! -f /etc/haproxy/hap.pem ]; then
    log "Generating SSL certificate..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/haproxy/hap.key \
    -out /etc/haproxy/hap.crt \
    -subj "/C=ID/ST=Jakarta/L=Jakarta/O=KedaiVPN/CN=$domain"

    # Combine key and certificate for HAProxy
    cat /etc/haproxy/hap.key /etc/haproxy/hap.crt > /etc/haproxy/hap.pem
    log "SSL certificate generated successfully"
fi

# Set proper permissions
chmod 600 /etc/haproxy/hap.pem
chown -R haproxy:haproxy /run/haproxy
chown -R haproxy:haproxy /var/lib/haproxy
log "Certificate permissions set"

# Backup original config
mv /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.bak

# Copy new config
cp haproxy.cfg /etc/haproxy/haproxy.cfg
log "Configuration file copied"

# Check config
log "Testing HAProxy configuration..."
if haproxy -c -f /etc/haproxy/haproxy.cfg; then
    log "Configuration test passed"
else
    log "Error: Configuration test failed"
    exit 1
fi

# Enable and start HAProxy service
systemctl enable haproxy
systemctl restart haproxy

# Show completion message
clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "          HAPROXY SETUP COMPLETED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Domain        : $domain"
echo "Certificate   : /etc/haproxy/hap.pem"
echo "Config File   : /etc/haproxy/haproxy.cfg"
echo ""
echo "HAProxy service is running and enabled"
echo ""
echo "Press any key to continue to main menu..."
read -n 1 -s -r
clear

# Show status
systemctl status haproxy
log "HAProxy started"

# Install and configure Nginx
log "Setting up Nginx..."
bash setup_nginx.sh

# Show completion message for both services
clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "     HAPROXY AND NGINX SETUP COMPLETED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "HAProxy Configuration: /etc/haproxy/haproxy.cfg"
echo "Nginx Configuration  : /etc/nginx/nginx.conf"
echo ""
echo "Both services are running and enabled"
echo ""