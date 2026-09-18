import os
import time
import logging
from logging.handlers import RotatingFileHandler

class CryptoFormatter(logging.Formatter):
    """Custom formatter injecting elapsed time and crypto emojis based on level."""
    LEVEL_EMOJIS = {
        logging.DEBUG: "🪙",
        logging.INFO: "🚀",
        logging.WARNING: "⚠️",
        logging.ERROR: "📉",
        logging.CRITICAL: "🚨"
    }

    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.start_time = time.time()

    def format(self, record):
        elapsed = time.time() - self.start_time
        record.elapsed = f"+{elapsed:.3f}s"
        record.emoji = self.LEVEL_EMOJIS.get(record.levelno, "🔹")
        return super().format(record)

def setup_logger(name: str = "crypto_tracker", log_file: str = "tracker.log") -> logging.Logger:
    """Sets up a rotating file logger with creative formatting for crypto ops."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    log_format = "%(asctime)s | %(elapsed)s | %(emoji)s %(levelname)-8s | %(message)s"
    formatter = CryptoFormatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_048_576,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

if __name__ == "__main__":
    log = setup_logger("test_tracker", "test_tracker.log")
    log.info("Starting up the engine...")
    time.sleep(0.12)
    log.warning("Bitcoin price fluctuation detected above threshold")
    time.sleep(0.05)
    log.error("Failed connection to trading exchange API")
    log.debug("Gas price currently at 35 Gwei")