import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

class CryptoLogger:
    def __init__(self, name: str = "crypto-tracker-38", log_file: str = "app.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s"
        )

        # Rotating handler: 5MB per file, keeping 3 backups
        handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=3
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Console stream for visual feedback during crypto swings
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

# Singleton for app-wide logging access
log = CryptoLogger().get_logger()

def log_trade_event(event: str, data: dict):
    timestamp = datetime.utcnow().isoformat()
    log.info(f"TRADE_EVENT: {event} | Payload: {data} | Time: {timestamp}")