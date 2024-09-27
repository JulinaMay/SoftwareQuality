import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime
from cryptography import *

# Ensure the directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Create a logger
logger = logging.getLogger('my_logger')
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)

    # Create a TimedRotatingFileHandler
    log_file = os.path.join('logs', 'MealManagement.log')
    handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=30)
    handler.setLevel(logging.INFO)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

# Function to log activities
def log_activity(username, description, additional_info=None, suspicious='No'):
    # Construct the log message based on provided information
    if additional_info:
        log_entry = f"{username} - {description} - {additional_info} - Suspicious: {suspicious}"
    else:
        log_entry = f"{username} {description} Suspicious: {suspicious}"

    if suspicious == 'Yes':
        logger.warning(log_entry)
    else:
        logger.info(log_entry)
