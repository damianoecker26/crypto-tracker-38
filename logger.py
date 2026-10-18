import logging
from logging.handlers import RotatingFileHandler
import sys
import os

def get_crypto_logger(name='crypto-tracker-38', log_file='crypto.log'):
    formatter = logging.Formatter(
        '[%(asctime)s] {%(levelname)s} (%(filename)s:%(lineno)d) -> %(message)s'
    )

    # Ensuring directory exists for our precious logs
    os.makedirs('logs', exist_ok=True)
    log_path = os.path.join('logs', log_file)

    # Rotating handler: 5MB per file, keep 3 backups
    handler = RotatingFileHandler(
        log_path, maxBytes=5*1024*1024, backupCount=3
    )
    handler.setFormatter(formatter)

    # Console output for the impatient developer
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console)

    return logger

# Instantiate the heartbeat of the tracker
logger = get_crypto_logger()