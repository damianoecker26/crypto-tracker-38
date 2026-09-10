import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name: str = "crypto-tracker-38"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_handler = RotatingFileHandler(
        "logs/crypto.log", 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

logger = get_crypto_logger()