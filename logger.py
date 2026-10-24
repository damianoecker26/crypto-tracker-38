import logging
import sys
from collections import deque
from typing import Any, Dict, Optional


class CryptoSymbolFormatter(logging.Formatter):
    """Custom formatter mapping log levels to crypto market indicators."""

    SYMBOLS = {
        logging.DEBUG: "🔍 [TICK]",
        logging.INFO: "📈 [INFO]",
        logging.WARNING: "⚠️  [VOLATILE]",
        logging.ERROR: "🚨 [DUMP]",
        logging.CRITICAL: "💥 [LIQUIDATION]",
    }

    def format(self, record: logging.LogRecord) -> str:
        symbol = self.SYMBOLS.get(record.levelno, "🪙")
        base_msg = super().format(record)
        return f"{symbol} {base_msg}"


class BufferedCryptoLogger:
    """A ring-buffered crypto event logger with automated spillover flushing."""

    def __init__(self, name: str, capacity: int = 50):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        self._buffer: deque = deque(maxlen=capacity)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            CryptoSymbolFormatter("%(asctime)s | %(name)s | %(message)s")
        )
        if not self._logger.handlers:
            self._logger.addHandler(handler)

    def log_trade(
        self, symbol: str, price: float, volume: float, side: str
    ) -> None:
        arrow = "🟢 BUY" if side.upper() == "BUY" else "🔴 SELL"
        payload = f"{symbol:<8} | {arrow} | P: {price:>10.4f} | V: {volume:>8.2f}"
        self._buffer.append(payload)

        if price <= 0:
            self._logger.error(f"Invalid price registered: {payload}")
        elif volume * price > 100_000:
            self._logger.warning(f"Whale movement detected: {payload}")
        else:
            self._logger.info(payload)

    def flush_history(self) -> list:
        history = list(self._buffer)
        self._buffer.clear()
        return history
