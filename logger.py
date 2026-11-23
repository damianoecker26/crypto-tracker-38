import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

class CryptoLogFormatter(logging.Formatter):
    EMOJI_MAP = {
        "INFO": "🪙 ",
        "WARNING": "⚠️ ",
        "ERROR": "🚨",
        "CRITICAL": "🔥",
        "DEBUG": "🔍"
    }

    def format(self, record: logging.LogRecord) -> str:
        prefix = self.EMOJI_MAP.get(record.levelname, "📌")
        record.msg = f"{prefix} {record.msg}"
        return super().format(record)

def setup_crypto_logger(
    name: str = "crypto_tracker",
    log_dir: str = "logs",
    max_bytes: int = 1_048_576,
    backup_count: int = 5
) -> logging.Logger:
    os.makedirs(log_dir, exist_ok=True)
    log_filepath = os.path.join(log_dir, f"{name}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = RotatingFileHandler(
        log_filepath,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    console_handler = logging.StreamHandler()

    fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    crypto_formatter = CryptoLogFormatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler.setFormatter(crypto_formatter)
    console_handler.setFormatter(crypto_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

crypto_logger = setup_crypto_logger()