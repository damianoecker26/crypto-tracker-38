import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        record.msg = f"[CRYPTO-38-LOG] {record.msg}"
        return super().format(record)

def setup_crypto_logger(log_path='logs/crypto_tracker.log'):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    logger = logging.getLogger('crypto_tracker')
    logger.setLevel(logging.DEBUG)
    
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    
    formatter = CryptoFormatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    # Console output for the impatient dev
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

logger = setup_crypto_logger()