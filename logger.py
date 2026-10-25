import gzip
import json
import logging
from logging.handlers import RotatingFileHandler
import os
import time


class CompressedCryptoRotator(RotatingFileHandler):
    """Custom log rotator that instantly gzips archives upon rollover."""

    def doRollover(self):
        super().doRollover()
        rotated_file = f"{self.baseFilename}.1"
        if os.path.exists(rotated_file):
            gz_file = f"{rotated_file}.gz"
            with open(rotated_file, "rb") as f_in:
                with gzip.open(gz_file, "wb") as f_out:
                    f_out.writelines(f_in)
            os.remove(rotated_file)


class CryptoLogFormatter(logging.Formatter):
    """Structured JSON formatter with crypto context annotations."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp_ms": int(record.created * 1000),
            "level": record.levelname,
            "channel": record.name,
            "msg": record.getMessage(),
        }
        if hasattr(record, "symbol"):
            log_entry["symbol"] = record.symbol
        if hasattr(record, "latency_ms"):
            log_entry["latency_ms"] = record.latency_ms
        return json.dumps(log_entry)


def setup_crypto_logger(name: str = "tracker", filename: str = "ticks.log") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = CompressedCryptoRotator(
            filename=filename,
            maxBytes=4096,
            backupCount=3,
            encoding="utf-8"
        )
        handler.setFormatter(CryptoLogFormatter())
        logger.addHandler(handler)

    return logger


if __name__ == "__main__":
    log = setup_crypto_logger()
    for i in range(50):
        log.info(
            "Processed Orderbook Snapshot",
            extra={"symbol": "BTC-USDT", "latency_ms": 12.4 + i}
        )
