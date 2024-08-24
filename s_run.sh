#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Set Flask environment variables
export FLASK_APP=run.py
echo " - Exported FLASK_APP to run.py"

export FLASK_ENV=development
echo " - Exported FLASK_ENV to "$FLASK_ENV

# Run the Flask application
echo " - Starting server "
flask run --host=0.0.0.0 --port=5002
