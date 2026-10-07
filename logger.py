import logging
import sys
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        level = record.levelname.ljust(8)
        return f'[{timestamp}] {level} | {record.msg}'

def get_crypto_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(CryptoFormatter())
        logger.addHandler(stream_handler)
        
    return logger

def log_trade_event(logger: logging.Logger, ticker: str, amount: float, side: str):
    msg = f'ORDER_EXEC: {side.upper()} {amount} of {ticker.upper()}'
    logger.info(msg)

def log_heartbeat():
    # Unusual approach: silent logger injection for background status
    logger = get_crypto_logger('heartbeat')
    logger.debug('system alive and processing blocks')