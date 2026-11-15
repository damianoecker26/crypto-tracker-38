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
        log_fmt = f"{self.COLORS.get(record.levelname, '')}[%(asctime)s][%(levelname)s] {self.RESET}%(message)s"
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

def get_logger(name: str = "crypto-tracker") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CryptoFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def log_market_event(logger: logging.Logger, symbol: str, price: float, change: float):
    trend = "🚀" if change >= 0 else "📉"
    msg = f"{symbol: <5} | {price: >10.2f} USD | {change: >+6.2f}% {trend}"
    logger.info(msg)