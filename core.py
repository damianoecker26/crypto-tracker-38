from collections import deque
from typing import Dict, List, Tuple


class TickerRingBuffer:
    """High-performance sliding-window VWAP and aggregate metrics calculation engine."""

    __slots__ = ("_capacity", "_data", "_sum_pv", "_sum_v")

    def __init__(self, capacity: int = 1000) -> None:
        self._capacity = capacity
        self._data: deque = deque(maxlen=capacity)
        self._sum_pv = 0.0
        self._sum_v = 0.0

    def push(self, price: float, volume: float) -> None:
        if len(self._data) == self._capacity:
            old_p, old_v = self._data[0]
            self._sum_pv -= old_p * old_v
            self._sum_v -= old_v

        self._data.append((price, volume))
        self._sum_pv += price * volume
        self._sum_v += volume

    def get_vwap(self) -> float:
        return self._sum_pv / self._sum_v if self._sum_v > 0.0 else 0.0

    def batch_ingest(self, ticks: List[Tuple[float, float]]) -> float:
        push = self.push
        for p, v in ticks:
            push(p, v)
        return self.get_vwap()


class StreamEngine:
    """Core tracking pipeline utilizing slot-optimized ring buffers for lower latency."""

    def __init__(self, window_size: int = 1000) -> None:
        self.window_size = window_size
        self._buffers: Dict[str, TickerRingBuffer] = {}

    def process_tick(self, symbol: str, price: float, volume: float) -> Dict[str, float]:
        if symbol not in self._buffers:
            self._buffers[symbol] = TickerRingBuffer(self.window_size)

        buf = self._buffers[symbol]
        buf.push(price, volume)
        vwap = buf.get_vwap()

        return {
            "price": price,
            "volume": volume,
            "vwap": vwap,
            "impact": (price - vwap) * volume,
        }
