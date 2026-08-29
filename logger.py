import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path
from datetime import datetime

def setup_logger(name="crypto_tracker_38", log_dir="logs", max_bytes=5242880, backup_count=3, log_level=logging.DEBUG):
    timestamp = datetime.now().strftime("%Y%m%d")
    full_log_dir = Path(log_dir) / timestamp
    full_log_dir.mkdir(parents=True, exist_ok=True)
    log_file = full_log_dir / f"{name}.log"
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.handlers = []
    file_handler = RotatingFileHandler(str(log_file), maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s | %(name)s | LEVEL:%(levelname)s | MSG:%(message)s | HASH:%(process)d%(thread)d")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.info("Logger initialized with rotation support")
    return logger

def get_logger(name="crypto_tracker_38"):
    return logging.getLogger(name)