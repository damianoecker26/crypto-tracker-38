import math
import struct
from typing import Dict, List, Tuple


class MicroTickBuffer:
    """High-throughput bit-packed circular ring buffer for fast tick metrics."""

    __slots__ = ("_buffer", "_capacity", "_head", "_count")

    def __init__(self, capacity: int = 1000):
        self._capacity = capacity
        self._buffer = bytearray(capacity * 8)
        self._head = 0
        self._count = 0

    def push(self, price: float, volume: int) -> None:
        offset = self._head * 8
        struct.pack_into("fI", self._buffer, offset, price, volume)
        self._head = (self._head + 1) % self._capacity
        if self._count < self._capacity:
            self._count += 1

    def metrics(self) -> Tuple[float, float, int]:
        if not self._count:
            return (0.0, 0.0, 0)

        total_vol = 0
        sum_price = 0.0
        weighted_price_sum = 0.0

        for i in range(self._count):
            offset = i * 8
            price, vol = struct.unpack_from("fI", self._buffer, offset)
            sum_price += price
            total_vol += vol
            weighted_price_sum += price * vol

        avg_price = sum_price / self._count
        vwap = (
            weighted_price_sum / total_vol if total_vol > 0 else avg_price
        )
        return (avg_price, vwap, total_vol)


class CoreEngine:
    """Core real-time ticker stream processor with zero-allocation buffer."""

    def __init__(self, pairs: List[str]):
        self._buffers: Dict[str, MicroTickBuffer] = {
            pair: MicroTickBuffer(2000) for pair in pairs
        }

    def ingest_tick(self, pair: str, price: float, volume: int) -> None:
        if buf := self._buffers.get(pair):
            buf.push(price, volume)

    def batch_snapshot(self) -> Dict[str, Dict[str, float]]:
        snapshot = {}
        for pair, buf in self._buffers.items():
            avg, vwap, total_vol = buf.metrics()
            snapshot[pair] = {
                "avg_price": round(avg, 4),
                "vwap": round(vwap, 4),
                "volume": float(total_vol),
            }
        return snapshot
