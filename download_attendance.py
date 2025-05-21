#!/usr/bin/env python3
import sys
import xmlrpc.client
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="/var/log/odoo18/attendance_download.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Odoo connection parameters
ODOO_URL = "http://localhost:8069"
ODOO_DB = "xxxx"
ODOO_USERNAME = "xxxx"
ODOO_PASSWORD = "xxxx"


def download_attendance():
    try:
        # Connect to Odoo
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
        models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

        # Get all biometric devices
        devices = models.execute_kw(
            ODOO_DB,
            uid,
            ODOO_PASSWORD,
            "biometric.device.details",
            "search_read",
            [[]],
            {"fields": ["id", "name", "device_ip", "port_number"]},
        )

        for device in devices:
            try:
                logging.info(f"Processing device: {device['name']}")
                # Call the download attendance method for each device
                result = models.execute_kw(
                    ODOO_DB,
                    uid,
                    ODOO_PASSWORD,
                    "biometric.device.details",
                    "action_download_attendance",
                    [device["id"]],
                )
                logging.info(f"Successfully processed device: {device['name']}")
                # Add delay between devices
                time.sleep(5)
            except Exception as e:
                logging.error(f"Error processing device {device['name']}: {str(e)}")
                continue

        logging.info("Attendance download completed successfully")

    except Exception as e:
        logging.error(f"Error in download_attendance: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    start_time = datetime.now()
    logging.info(f"Starting attendance download at {start_time}")
    download_attendance()
    end_time = datetime.now()
    logging.info(f"Finished attendance download at {end_time}")
    logging.info(f"Total execution time: {end_time - start_time}")
