import array
from typing import Dict, List, Tuple

class FastTickerBuffer:
    """Pre-allocated circular byte buffer for high-frequency tick processing."""
    __slots__ = ('_capacity', '_buffer', '_head', '_count', '_sum_price', '_sum_vol')

    def __init__(self, capacity: int = 1024):
        self._capacity = capacity
        self._buffer = array.array('d', [0.0] * (capacity * 2))
        self._head = 0
        self._count = 0
        self._sum_price = 0.0
        self._sum_vol = 0.0

    def push(self, price: float, volume: float) -> None:
        idx = self._head * 2
        if self._count == self._capacity:
            self._sum_price -= self._buffer[idx]
            self._sum_vol -= self._buffer[idx + 1]
        else:
            self._count += 1

        self._buffer[idx] = price
        self._buffer[idx + 1] = volume
        self._sum_price += price
        self._sum_vol += volume
        self._head = (self._head + 1) % self._capacity

    def vwap(self) -> float:
        return self._sum_price / self._sum_vol if self._sum_vol > 0 else 0.0

    def snapshot(self) -> List[Tuple[float, float]]:
        if self._count == 0:
            return []
        start = (self._head - self._count) % self._capacity
        return [
            (self._buffer[((start + i) % self._capacity) * 2], 
             self._buffer[((start + i) % self._capacity) * 2 + 1])
            for i in range(self._count)
        ]

class MarketDataEngine:
    """High-throughput multi-pair crypto feed processor."""

    def __init__(self, buffer_size: int = 500):
        self._buffers: Dict[str, FastTickerBuffer] = {}
        self._buffer_size = buffer_size

    def ingest_trade(self, symbol: str, price: float, volume: float) -> float:
        if symbol not in self._buffers:
            self._buffers[symbol] = FastTickerBuffer(self._buffer_size)
        buf = self._buffers[symbol]
        buf.push(price, volume)
        return buf.vwap()

    def batch_vwap(self) -> Dict[str, float]:
        return {sym: buf.vwap() for sym, buf in self._buffers.items()}
