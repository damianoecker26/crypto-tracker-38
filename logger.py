import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name: str = 'crypto-tracker-38') -> logging.Logger:
    log_path = os.getenv('LOG_DIR', './logs')
    os.makedirs(log_path, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s] | %(levelname)s | %(name)s | %(message)s'
        )
        
        # Rotates at 5MB, keeps 3 backups
        file_handler = RotatingFileHandler(
            os.path.join(log_path, 'crypto.log'),
            maxBytes=5*1024*1024,
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        
    return logger

# Quick access for crypto modules
crypto_logger = get_crypto_logger()