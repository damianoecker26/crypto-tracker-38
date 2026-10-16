import array
import time
from typing import Dict, Optional, Tuple

class RingBufferAggregator:
    """Zero-allocation sliding window calculation using native C-arrays."""
    __slots__ = ("capacity", "prices", "timestamps", "head", "size")

    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.prices = array.array('d', [0.0] * capacity)
        self.timestamps = array.array('d', [0.0] * capacity)
        self.head = 0
        self.size = 0

    def push(self, price: float, timestamp: Optional[float] = None) -> None:
        ts = timestamp if timestamp is not None else time.time()
        self.prices[self.head] = price
        self.timestamps[self.head] = ts
        self.head = (self.head + 1) % self.capacity
        if self.size < self.capacity:
            self.size += 1

    def compute_window_stats(self, window_seconds: float) -> Tuple[float, float, float]:
        if self.size == 0:
            return (0.0, 0.0, 0.0)
        
        cutoff = time.time() - window_seconds
        total, count = 0.0, 0
        min_p, max_p = float('inf'), float('-inf')
        
        idx = (self.head - 1) % self.capacity
        for _ in range(self.size):
            if self.timestamps[idx] < cutoff:
                break
            p = self.prices[idx]
            total += p
            if p < min_p: min_p = p
            if p > max_p: max_p = p
            count += 1
            idx = (idx - 1) % self.capacity

        return (total / count, min_p, max_p) if count > 0 else (0.0, 0.0, 0.0)

class StreamEngine:
    """Core processing module optimizing high-frequency crypto price feeds."""
    def __init__(self):
        self._pairs: Dict[str, RingBufferAggregator] = {}

    def process_tick(self, symbol: str, price: float) -> Dict[str, float]:
        if symbol not in self._pairs:
            self._pairs[symbol] = RingBufferAggregator(capacity=20000)
        
        buf = self._pairs[symbol]
        buf.push(price)
        avg_price, min_price, max_price = buf.compute_window_stats(window_seconds=60.0)
        return {"symbol": symbol, "vwap": round(avg_price, 4), "low": min_price, "high": max_price}
