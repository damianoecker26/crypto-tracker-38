import logging
from logging.handlers import RotatingFileHandler
import sys
import os

class CryptoFormatter(logging.Formatter):
    """Custom formatter to add vibe-based prefixes to logs."""
    vibes = {logging.INFO: '🚀', logging.ERROR: '🔥', logging.DEBUG: '🔍', logging.WARNING: '⚠️'}
    def format(self, record):
        vibe = self.vibes.get(record.levelno, '✨')
        return f"{vibe} [{record.levelname}] {record.msg}"

def setup_logger(name: str = "crypto-tracker-38", log_file: str = "crypto.log"):
    """Initialize log rotation for crypto-tracker-38 infrastructure."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        file_handler = RotatingFileHandler(
            log_file, maxBytes=1024*1024*5, backupCount=3
        )
        file_handler.setFormatter(CryptoFormatter())
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(CryptoFormatter())
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()