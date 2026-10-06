import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class CryptoLogger:
    def __init__(self, name='crypto-tracker-38', log_dir='logs'):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        log_path = os.path.join(log_dir, f'{name}.log')
        handler = RotatingFileHandler(
            log_path, 
            maxBytes=2 * 1024 * 1024, 
            backupCount=5
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

log = CryptoLogger().get_logger()

def log_trade_event(symbol, side, price):
    log.info(f'TRADE_EXECUTION: {side} {symbol} at {price}')