import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='crypto-tracker-38', path='logs/tracker.log'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Custom formatter for 'crypto-niche' feel
    formatter = logging.Formatter(
        '[%(asctime)s] ₿ %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Rotation logic: keep 5 files of 2MB each
    handler = RotatingFileHandler(
        path, 
        maxBytes=2*1024*1024, 
        backupCount=5
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        # Also output to stdout for real-time monitoring
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    
    return logger

# Singleton instance for quick app-wide access
crypto_logger = get_crypto_logger()