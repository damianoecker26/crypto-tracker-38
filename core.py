import math
from array import array
from typing import Dict, Optional


class FastTickerBuffer:
    """High-throughput ring buffer for crypto price tick updates with optimized stats calculation."""

    __slots__ = ("capacity", "_prices", "_timestamps", "_head", "_count", "_sum")

    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self._prices = array("d", [0.0] * capacity)
        self._timestamps = array("d", [0.0] * capacity)
        self._head = 0
        self._count = 0
        self._sum = 0.0

    def push(self, timestamp: float, price: float) -> None:
        if self._count == self.capacity:
            self._sum -= self._prices[self._head]
        else:
            self._count += 1

        self._prices[self._head] = price
        self._timestamps[self._head] = timestamp
        self._sum += price
        self._head = (self._head + 1) % self.capacity

    @property
    def mean(self) -> float:
        return self._sum / self._count if self._count > 0 else 0.0

    def calculate_volatility(self) -> float:
        if self._count < 2:
            return 0.0
        avg = self.mean
        variance_sum = sum((self._prices[i] - avg) ** 2 for i in range(self._count))
        return math.sqrt(variance_sum / (self._count - 1))

    def snapshot(self) -> Dict[str, float]:
        if self._count == 0:
            return {"latest": 0.0, "mean": 0.0, "volatility": 0.0}
        latest_idx = (self._head - 1) % self.capacity
        return {
            "latest": self._prices[latest_idx],
            "mean": round(self.mean, 4),
            "volatility": round(self.calculate_volatility(), 6),
        }


class CorePriceEngine:
    """Central processing engine for tracking dynamic ticker streams with zero-copy buffer."""

    def __init__(self, window_size: int = 500):
        self.buffers: Dict[str, FastTickerBuffer] = {}
        self.window_size = window_size

    def ingest_tick(self, symbol: str, timestamp: float, price: float) -> None:
        if symbol not in self.buffers:
            self.buffers[symbol] = FastTickerBuffer(self.window_size)
        self.buffers[symbol].push(timestamp, price)

    def get_market_metrics(self, symbol: str) -> Optional[Dict[str, float]]:
        buf = self.buffers.get(symbol)
        return buf.snapshot() if buf else None
