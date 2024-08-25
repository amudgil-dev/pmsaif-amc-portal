#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if the service file exists
if [ -f /home/ubuntu/pmsweb2/remote_service/pmsportal.service ]; then
    echo "pmsportal.service file  found. Please update service file ."
    exit 1
fi

# Move the service file to the systemd directory
sudo mv /home/ubuntu/pmsweb/remote_service/pmsportal.service /etc/systemd/system/

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Check if the service is already running
if systemctl is-active --quiet pmsportal; then
    echo "PMS Portal service is already running."
else
    # Start the pmsportal service
    sudo systemctl start pmsportal
    echo "PMS Portal service has been started."
fi

# Enable the service to start on boot
sudo systemctl enable pmsportal

# Check the status of the service
sudo systemctl status pmsportal

echo "PMS Portal service has been set up and started. Check the status output above for any issues."