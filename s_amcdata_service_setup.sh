#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if the service file exists
# if [ -f /home/ubuntu/amcdata/remote_service/amcdata.service ]; then
#     echo "amcdata_service.service file  found. Please update service file ."
#     exit 1
# fi

# Move the service file to the systemd directory
sudo mv /home/ubuntu/amcdata/remote_service/amcdata.service /etc/systemd/system/

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Check if the service is already running
if systemctl is-active --quiet amcdata; then
    echo "amcdata Portal service is already running."
else
    # Start the amcdata_service service
    sudo systemctl start amcdata
    echo "amcdata Portal service has been started."
fi

# Enable the service to start on boot
sudo systemctl enable amcdata

# Check the status of the service
sudo systemctl status amcdata

echo "amcdata  portal service has been set up and started. Check the status output above for any issues."