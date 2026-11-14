import logging
import sys
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[41m'
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        timestamp = datetime.now().strftime('%H:%M:%S')
        return f"{log_color}[{timestamp}] {record.levelname}: {record.getMessage()}{self.RESET}"

def get_crypto_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CryptoFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger

setup_logger = get_crypto_logger("crypto-tracker-38")