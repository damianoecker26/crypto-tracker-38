import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

class CryptoLogger:
    def __init__(self, name: str = 'crypto-tracker-38', log_dir: str = 'logs'):
        self.log_path = Path(log_dir)
        self.log_path.mkdir(exist_ok=True)
        self.file_path = self.log_path / f'{name}.log'
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._setup_handlers()

    def _setup_handlers(self):
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [crypto-node] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler = RotatingFileHandler(
            self.file_path, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

logger = CryptoLogger().get_logger()