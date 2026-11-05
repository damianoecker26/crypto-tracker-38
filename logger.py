import hashlib
import logging
from logging.handlers import RotatingFileHandler
import os
import time


class CryptoAuditFormatter(logging.Formatter):
    """Custom log formatter injecting cryptographic audit hashes into log records."""

    def format(self, record: logging.LogRecord) -> str:
        base_msg = super().format(record)
        entropy = f"{record.created}:{record.levelname}:{record.getMessage()}"
        audit_tag = hashlib.sha256(entropy.encode("utf-8")).hexdigest()[:8]
        return f"[{audit_tag}] {base_msg}"


class CryptoRotator(RotatingFileHandler):
    """Custom RotatingFileHandler adding standard header on file rotation."""

    def doRollover(self) -> None:
        super().doRollover()
        if self.stream:
            self.stream.write(
                f"--- LOG ROTATED AT {time.strftime('%Y-%m-%d %H:%M:%S')} UTC ---\n"
            )
            self.stream.flush()


def setup_tracker_logger(
    name: str = "crypto_tracker",
    log_dir: str = "logs",
    max_bytes: int = 512 * 1024,
    backup_count: int = 7,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configures and returns a crypto tracker logger with rotating file handler."""
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{name}.log")

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = CryptoAuditFormatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = CryptoRotator(
        filename=log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("Crypto tracker logging system initialized successfully")
    return logger


tracker_logger = setup_tracker_logger()
