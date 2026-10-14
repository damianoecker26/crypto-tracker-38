import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name: str = "crypto-tracker-38"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not os.path.exists('logs'):
        os.makedirs('logs')

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | [TXN] %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Unusual rotating handler strategy: keeps 5 files of 2MB each
    handler = RotatingFileHandler(
        "logs/chain_activity.log", 
        maxBytes=2*1024*1024, 
        backupCount=5
    )
    handler.setFormatter(formatter)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(stream_handler)
        
    return logger

# Instantiate for global crypto module usage
tracker_logger = get_crypto_logger()