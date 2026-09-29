import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_crypto_logger(name: str) -> logging.Logger:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    
    file_path = log_dir / "crypto_tracker.log"
    
    # Using a 5MB rotation strategy for high-frequency price updates
    handler = RotatingFileHandler(
        file_path, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=5
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # console echo for live monitoring in development
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

# Instantiate the heartbeat monitor
logger = get_crypto_logger("crypto-tracker-38")