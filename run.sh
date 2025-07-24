#!/bin/bash

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Check if port 5000 is in use and kill the process
if lsof -i:5000 -t; then
    echo "Port 5000 is in use. Attempting to kill the process..."
    kill -9 $(lsof -i:5000 -t)
    sleep 2 # Give the OS a moment to release the port
fi

# Run the application
export FLASK_APP=api/index.py
flask run
