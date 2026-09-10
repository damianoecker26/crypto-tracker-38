import logging
from logging.handlers import RotatingFileHandler

class CryptoFormatter(logging.Formatter):
    """Custom formatter that auto-highlights potential crypto tickers in logs."""
    def format(self, record):
        if isinstance(record.msg, str):
            words = record.msg.split()
            processed = [f"[{w}]" if w.isupper() and 3 <= len(w) <= 5 else w for w in words]
            record.msg = " ".join(processed)
        return super().format(record)

def setup_logger(name="crypto_tracker", log_file="tracker.log"):
    """Initializes a rotating logger with a dual destination output topology."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=1024 * 1024 * 2, 
            backupCount=3, 
            encoding="utf-8"
        )
        formatter = CryptoFormatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    return logger