import logging
import sys
from typing import Any, Dict

class CryptoLogger:
    """Custom logger for crypto-tracker-38 events."""
    
    def __init__(self, name: str = "tracker") -> None:
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        formatter: logging.Formatter = logging.Formatter(
            "[%(asctime)s] {%(levelname)s} -> %(message)s", datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_trade(self, symbol: str, data: Dict[str, Any]) -> None:
        """Log specific trade activity with market details."""
        self.logger.info(f"Trade captured for {symbol.upper()}: {data}")

    def log_error(self, message: str, context: Dict[str, Any] | None = None) -> None:
        """Standardized reporting for chain/API interruptions."""
        details: str = f" | Context: {context}" if context else ""
        self.logger.error(f"CRITICAL FAILURE: {message}{details}")

logger: CryptoLogger = CryptoLogger()