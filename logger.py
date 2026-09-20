import json
import logging
from logging.handlers import RotatingFileHandler
import os
import gzip
import shutil

class CryptoGzipRotatingFileHandler(RotatingFileHandler):
    """
    A custom rotating file handler that compresses old log files using gzip
    automatically upon rollover, keeping the crypto-tracker-38 storage lightweight.
    """
    def doRollover(self):
        super().doRollover()
        for i in range(self.backupCount, 0, -1):
            sfn = f"{self.baseFilename}.{i}"
            dfn = f"{sfn}.gz"
            if os.path.exists(sfn) and not os.path.exists(dfn):
                with open(sfn, 'rb') as f_in:
                    with gzip.open(dfn, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(sfn)

class CryptoLogFormatter(logging.Formatter):
    """
    Format logs with distinct crypto emojis based on the log level
    to monitor pipeline health in real-time.
    """
    LEVEL_EMOJIS = {
        logging.DEBUG: "🔍",
        logging.INFO: "📈",
        logging.WARNING: "⚠️",
        logging.ERROR: "🚨",
        logging.CRITICAL: "💥"
    }

    def format(self, record):
        emoji = self.LEVEL_EMOJIS.get(record.levelno, "📝")
        ticker = getattr(record, "ticker", "SYS")
        record.msg = f"[{ticker}] {emoji} {record.msg}"
        return super().format(record)

def setup_tracker_logger(name="crypto-tracker", log_file="tracker.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = CryptoLogFormatter("%(asctime)s | %(levelname)-8s | %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    file_handler = CryptoGzipRotatingFileHandler(
        log_file, maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger