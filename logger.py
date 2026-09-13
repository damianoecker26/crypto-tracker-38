import logging
import sys
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    COLORS = {'INFO': '\033[94m', 'ERROR': '\033[91m', 'DEBUG': '\033[92m', 'WARNING': '\033[93m'}
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        log_msg = super().format(record)
        return f"{color}[{datetime.now().strftime('%H:%M:%S')}] {log_msg}{self.RESET}"

def setup_crypto_logger(name: str = 'crypto-tracker'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CryptoFormatter('%(levelname)s | %(name)s | %(message)s'))
    
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger

logger = setup_crypto_logger()