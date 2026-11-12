import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import hashlib
import time

class CryptoLogFormatter(logging.Formatter):
    """Custom log formatter that attaches a lightweight crypto hash signature to log entries."""
    
    def format(self, record):
        base_msg = super().format(record)
        nonce = int(time.time() * 1000) % 100000
        hash_digest = hashlib.sha256(f"{nonce}:{base_msg}".encode()).hexdigest()[:8]
        return f"[{hash_digest}] {base_msg}"

class DynamicCryptoLogger:
    """Logger manager providing size-rotated log files with custom integrity formatting."""
    
    def __init__(self, name: str = "crypto_tracker", log_dir: str = "logs"):
        self.name = name
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def build_logger(self, max_mb: int = 5, backup_count: int = 3, level: int = logging.INFO) -> logging.Logger:
        logger = logging.getLogger(self.name)
        logger.setLevel(level)
        logger.handlers.clear()

        formatter = CryptoLogFormatter(
            fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        log_file = os.path.join(self.log_dir, f"{self.name}.log")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_mb * 1024 * 1024,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger

def setup_logger(name: str = "crypto_tracker") -> logging.Logger:
    return DynamicCryptoLogger(name=name).build_logger()
