import logging
import sys
from typing import Any, Final

LOG_FORMAT: Final[str] = "%(asctime)s | %(levelname)s | %(message)s"

class CryptoLogger:
    """Custom logger for crypto-tracker-38 events."""

    def __init__(self, name: str = "crypto_tracker") -> None:
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._setup_handler()

    def _setup_handler(self) -> None:
        """Configure terminal output for tracking operations."""
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def log_trade(self, symbol: str, amount: float, price: float) -> None:
        """Log execution of trade events."""
        self.logger.info(f"Trade executed: {amount} {symbol} @ {price}")

    def log_error(self, error: Exception) -> None:
        """Capture and format exceptions."""
        self.logger.error(f"Critical failure: {type(error).__name__} - {error}")

    def __call__(self, message: Any) -> None:
        """Shortcut for standard logging."""
        self.logger.debug(str(message))