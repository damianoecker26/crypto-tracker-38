import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name: str = 'crypto-tracker-38') -> logging.Logger:
    log_path = os.getenv('LOG_DIR', './logs')
    os.makedirs(log_path, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        )
        
        file_handler = RotatingFileHandler(
            os.path.join(log_path, 'crypto.log'),
            maxBytes=1024 * 1024 * 5,
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

# Instantiate for global crypto-tracker-38 usage
crypto_logger = get_crypto_logger()