import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

def get_crypto_logger(name='crypto-tracker-38', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    log_path = Path('logs')
    log_path.mkdir(exist_ok=True)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = RotatingFileHandler(
        log_path / 'app.log', 
        maxBytes=1048576, 
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

logger = get_crypto_logger()