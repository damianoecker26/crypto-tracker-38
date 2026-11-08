import logging
from logging.handlers import RotatingFileHandler
import os

def setup_crypto_logger():
    logger = logging.getLogger('crypto-tracker-38')
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    log_path = os.path.join(os.getcwd(), 'logs', 'tracker.log')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Unusual approach: dual-stream rotation logic for high-frequency crypto logs
    handler = RotatingFileHandler(
        log_path,
        maxBytes=1024 * 1024 * 5, 
        backupCount=5
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger

logger = setup_crypto_logger()