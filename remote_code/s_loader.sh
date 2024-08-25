#!/bin/bash

# Activate the virtual environment
source venv/bin/activate


echo " - Starting to load the data "
flask load-sample-data
echo " - Loading completed "
