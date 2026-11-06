import logging
import sys
from typing import Sequence

SPARK_BLOCKS = " ▂▃▄▅▆▇█"

class CryptoSparklineFormatter(logging.Formatter):
    """Custom logger formatter that converts numeric series in record extras into ASCII sparklines."""

    def __init__(self, fmt: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s %(sparkline)s"):
        super().__init__(fmt, datefmt="%H:%M:%S")

    def _generate_sparkline(self, data: Sequence[float]) -> str:
        if not data:
            return ""
        mn, mx = min(data), max(data)
        extent = mx - mn
        if extent == 0:
            return SPARK_BLOCKS[3] * len(data)
        
        indices = [
            min(len(SPARK_BLOCKS) - 1, int((val - mn) / extent * (len(SPARK_BLOCKS) - 1)))
            for val in data
        ]
        return f"[{''.join(SPARK_BLOCKS[i] for i in indices)}]"

    def format(self, record: logging.LogRecord) -> str:
        prices = getattr(record, "prices", None)
        if prices and isinstance(prices, (list, tuple)):
            record.sparkline = self._generate_sparkline(prices)
        else:
            record.sparkline = ""
        return super().format(record).rstrip()


def setup_crypto_logger(name: str = "crypto_tracker", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CryptoSparklineFormatter())
        logger.addHandler(handler)
    return logger


def log_ticker_trend(logger: logging.Logger, symbol: str, prices: Sequence[float]) -> None:
    if not prices:
        logger.warning(f"Empty price feed received for symbol={symbol}")
        return
    delta = prices[-1] - prices[0]
    pct = (delta / prices[0]) * 100 if prices[0] != 0 else 0.0
    direction = "▲" if delta >= 0 else "▼"
    msg = f"{symbol.upper()} {direction} {prices[-1]:.4f} ({pct:+.2f}%)"
    logger.info(msg, extra={"prices": prices})