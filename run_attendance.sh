#!/bin/bash

# Activate virtual environment if you're using one
source /opt/odoo18/venv/bin/activate

# Set environment variables
export PYTHONPATH="/opt/odoo18:/opt/odoo18/venv/lib/python3.10/site-packages"
export PATH=$PATH:/usr/local/bin

# Create log directory if it doesn't exist
mkdir -p /var/log/odoo18

# Run the script
/opt/odoo18/scripts/download_attendance.py

# Deactivate virtual environment
deactivate

