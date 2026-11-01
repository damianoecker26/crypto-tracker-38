import logging
import sys
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    COLORS = {'DEBUG': '36', 'INFO': '32', 'WARNING': '33', 'ERROR': '31', 'CRITICAL': '35'}
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, '37')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f'\033[{color}m[{timestamp}] {record.levelname}: {record.getMessage()}\033[0m'

def setup_crypto_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CryptoFormatter())
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

log = setup_crypto_logger('crypto-tracker-38')

if __name__ == '__main__':
    log.info('logger initialized for crypto-tracker-38')