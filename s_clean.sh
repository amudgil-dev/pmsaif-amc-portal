#!/bin/bash


source deactivate
echo " - Deactivated venv"

# Remove all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} +

# Remove the venv directory
rm -rf venv

echo " - Removed venv"

# Remove the logs directory and all log files
rm -rf logs
find . -type f -name "*.log" -delete
echo " - Removed all logs and logs folder"

echo " - Cleaned up __pycache__ directories and venv folder."