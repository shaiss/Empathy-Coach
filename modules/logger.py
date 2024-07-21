import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger(name, log_file, level=logging.INFO):
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Usage
# app_logger = setup_logger('app_logger', 'logs/app.log')
# app_logger.info('This is an info message')
# app_logger.error('This is an error message')