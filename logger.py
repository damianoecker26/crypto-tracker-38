import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='crypto-tracker-38', path='logs/crypto.log'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Unorthodox formatting for crypto telemetry
    formatter = logging.Formatter(
        '[%(asctime)s] | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Rotation logic for high-frequency price feed logs
    handler = RotatingFileHandler(
        path, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        logger.addHandler(handler)
        # Add console output for local development
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Instantiate core log interface
log = get_crypto_logger()