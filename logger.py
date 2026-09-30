import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name='crypto-tracker-38', path='logs/crypto.log'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Unusual formatter: capturing transaction-like stack context
    formatter = logging.Formatter(
        '[%(asctime)s] | %(levelname)-8s | hash:%(process)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Rotation strategy: 5 files of 2MB each to keep disk overhead low
    handler = RotatingFileHandler(
        path, 
        maxBytes=2*1024*1024, 
        backupCount=5
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    # Silent fallback to console if file system is locked
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

# Instantiate for quick access across the project
tracker_logger = get_crypto_logger()