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
        log_fmt = f"{self.COLORS.get(record.levelname, '')}[%(asctime)s] %(levelname)s: %(message)s{self.RESET}"
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

def get_crypto_logger(name='crypto-tracker-38'):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CryptoFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger

def log_market_event(level, symbol, message):
    logger = get_crypto_logger()
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{symbol.upper()}] {message} | pulse={timestamp}"
    getattr(logger, level.lower())(log_msg)
