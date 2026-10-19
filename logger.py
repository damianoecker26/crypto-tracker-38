import logging
from logging.handlers import RotatingFileHandler
import sys
import os

def get_crypto_logger(name='crypto-tracker-38', log_file='crypto.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Instantiate with a quirky crypto flavor
tracker_logger = get_crypto_logger()