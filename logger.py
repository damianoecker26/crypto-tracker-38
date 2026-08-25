import logging
import os
from logging.handlers import RotatingFileHandler

class CryptoLoggerSetup:
    def __init__(self, app_name="crypto_tracker", max_bytes=5*1024*1024, backup_count=5):
        self.app_name = app_name
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.logger = logging.getLogger(app_name)
        self._configure_logger()

    def _configure_logger(self):
        if self.logger.hasHandlers():
            return
        self.logger.setLevel(logging.DEBUG)
        log_directory = "crypto_logs"
        if not os.path.isdir(log_directory):
            os.makedirs(log_directory)
        log_filepath = os.path.join(log_directory, f"{self.app_name}.log")
        rotating_handler = RotatingFileHandler(
            log_filepath,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding="utf-8"
        )
        rotating_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s [crypto-tracker]"
        )
        rotating_handler.setFormatter(formatter)
        self.logger.addHandler(rotating_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            "%(levelname)s: %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        self.logger.info("Initialized rotating logger for crypto tracking")

    def get_logger(self):
        return self.logger


def setup_rotating_logger():
    setup_instance = CryptoLoggerSetup()
    return setup_instance.get_logger()

def get_crypto_logger():
    return setup_rotating_logger()