import logging
from typing import Any, Final

# Crypto-tracker-38 custom logging protocol
LEVEL_MAP: Final[dict[str, int]] = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "error": logging.ERROR
}

def setup_crypto_logger(name: str = "tracker_node") -> logging.Logger:
    """
    Initializes a custom console logger for blockchain-related events.
    Returns a pre-configured logging instance.
    """
    logger: logging.Logger = logging.getLogger(name)
    handler: logging.StreamHandler = logging.StreamHandler()
    formatter: logging.Formatter = logging.Formatter(
        "[%(asctime)s] | CRYPTO-LOG | %(levelname)s | %(message)s"
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def log_trade_event(logger: logging.Logger, pair: str, status: str, details: Any) -> None:
    """
    Formats and transmits trade-specific diagnostic data to the stream.
    """
    log_msg: str = f"Event: {pair} -> Status: {status} | Data: {details}"
    logger.info(log_msg)

logger: logging.Logger = setup_crypto_logger()