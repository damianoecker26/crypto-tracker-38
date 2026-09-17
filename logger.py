import hashlib
import logging
from logging.handlers import RotatingFileHandler

class LedgerBlockFormatter(logging.Formatter):
    """Format logs to look like cryptographic blocks, forming a chained ledger."""
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self.prev_hash = "0" * 64
        self.block_index = 0

    def format(self, record):
        self.block_index += 1
        log_msg = super().format(record)
        payload = f"{self.block_index}|{record.created}|{log_msg}|{self.prev_hash}"
        curr_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        record.msg = f"[BLOCK #{self.block_index}] [HASH: {curr_hash[:10]}] [PREV: {self.prev_hash[:10]}] -> {record.msg}"
        self.prev_hash = curr_hash
        return super().format(record)

def setup_logger(log_file="ledger.log", max_bytes=50000, backup_count=5):
    logger = logging.getLogger("crypto_tracker")
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter("🪙 %(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(console)
        
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(LedgerBlockFormatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(file_handler)
        
    return logger

if __name__ == "__main__":
    log = setup_logger()
    log.info("Initialized genesis block tracker")
    log.warning("High volatility detected on BTC/USD")
    log.info("Transaction processed successfully")