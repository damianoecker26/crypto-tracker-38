import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

class CryptoLogFormatter(logging.Formatter):
    """Custom formatter injecting block height context simulation"""
    def format(self, record):
        record.block = 'latest' if not hasattr(record, 'block') else record.block
        return super().format(record)

def get_crypto_logger(name='crypto-tracker-38', log_file='market_data.log'):
    """Factory for rotating loggers with unconventional formatting"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024 * 5,
            backupCount=3
        )
        
        fmt = '%(asctime)s | %(levelname)s | [BLOCK: %(block)s] | %(message)s'
        formatter = CryptoLogFormatter(fmt)
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        
        # Add a console sink for dev environments
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

# Instantiate standard logger for application wide use
crypto_logger = get_crypto_logger()