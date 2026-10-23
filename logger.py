import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict


class CryptoLogFormatter(logging.Formatter):
    """Custom log formatter decorating entries with crypto status indicators."""

    INDICATORS = {
        "DEBUG": "🔍",
        "INFO": "⚡",
        "WARNING": "⚠️",
        "ERROR": "🚨",
        "CRITICAL": "💥",
    }

    def format(self, record: logging.LogRecord) -> str:
        icon = self.INDICATORS.get(record.levelname, "📌")
        payload: Dict[str, Any] = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "icon": icon,
            "scope": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def setup_crypto_logger(
    name: str = "crypto_tracker",
    log_dir: str = "logs",
    max_bytes: int = 2 * 1024 * 1024,
    backup_count: int = 5,
) -> logging.Logger:
    """Configures a rotating JSON logger for high-throughput market streams."""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        file_handler = RotatingFileHandler(
            filename=log_path / f"{name}.jsonl",
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(CryptoLogFormatter())
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(
            logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
        )

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    log = setup_crypto_logger()
    log.info("Ingesting orderbook snapshot for BTC/USDT")
    log.warning("High price slippage detected: 2.4%")
