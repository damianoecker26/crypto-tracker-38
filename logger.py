import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

def get_crypto_logger(name: str = "crypto-tracker-38") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.hasHandlers():
        return logger

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = RotatingFileHandler(
        log_dir / "tracker.log",
        maxBytes=1024 * 1024 * 5,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.propagate = False
    return logger

crypto_logger = get_crypto_logger()