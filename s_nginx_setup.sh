#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting Nginx installation and configuration..."

# Update package list and install Nginx
sudo apt-get update
sudo apt-get install -y nginx

echo "Nginx installed successfully."

# Create Nginx configuration file for pmsservice
sudo tee /etc/nginx/sites-available/pmsportal > /dev/null <<EOT
upstream pmsportal_app {
    server unix:/home/ubuntu/pmsweb2/pmsportal.sock;
}

# Define the second upstream for your other service
# upstream second_service {
    # server unix:/path/to/your/second_service.sock;
    # If your second service uses a network socket instead, use this:
    # server 127.0.0.1:8001;
# }


server {
    listen 80;
    server_name 52.66.87.168;

    location / {
        proxy_set_header Host \$http_host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_pass http://pmsportal_app;
    }
    # Configuration for the second service
    # location /second_service/ {
    #     proxy_set_header Host $http_host;
    #     proxy_set_header X-Real-IP $remote_addr;
    #     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    #     proxy_set_header X-Forwarded-Proto $scheme;
    #     proxy_pass http://second_service;
    # }    
}
EOT

echo "Nginx configuration file created."

# Create symbolic link to enable the site
sudo ln -sf /etc/nginx/sites-available/pmsportal /etc/nginx/sites-enabled

echo "Nginx site enabled."

# Remove default Nginx site
sudo rm -f /etc/nginx/sites-enabled/default

echo "Default Nginx site removed."

# Test Nginx configuration
sudo nginx -t

echo "Nginx configuration test completed."

# Reload Nginx to apply new configuration
sudo systemctl reload nginx

echo "Nginx reloaded with new configuration."

# Check Nginx status
sudo systemctl status nginx

echo "Nginx installation and configuration completed. Please check the status output above for any issues."