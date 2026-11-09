import sys
import logging
from typing import Any, Dict

class CryptoSignalFormatter(logging.Formatter):
    """Custom logging formatter that injects visual crypto trend indicators based on record context."""

    BADGES = {
        "bullish": "\u001b[92m[▲ BULLISH]\u001b[0m",
        "bearish": "\u001b[91m[▼ BEARISH]\u001b[0m",
        "spike": "\u001b[93m[⚡ SPIKE]\u001b[0m",
        "neutral": "\u001b[94m[⚓ NEUTRAL]\u001b[0m"
    }

    def format(self, record: logging.LogRecord) -> str:
        delta = getattr(record, 'price_change', 0.0)
        volume = getattr(record, 'volume_surge', False)

        if volume and abs(delta) > 5.0:
            badge = self.BADGES["spike"]
        elif delta > 1.5:
            badge = self.BADGES["bullish"]
        elif delta < -1.5:
            badge = self.BADGES["bearish"]
        else:
            badge = self.BADGES["neutral"]

        formatted_msg = super().format(record)
        return f"{badge} {formatted_msg}"


def setup_crypto_logger(name: str = "crypto_tracker", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = CryptoSignalFormatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def log_market_event(logger: logging.Logger, ticker: str, price: float, change_24h: float, volume_surge: bool = False) -> None:
    message = f"[{ticker.upper()}] ${price:,.2f} ({change_24h:+.2f}%)"
    logger.info(message, extra={"price_change": change_24h, "volume_surge": volume_surge})
