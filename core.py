import array
import time
from typing import Iterator, NamedTuple


class TickerBatch(NamedTuple):
    symbol: str
    avg_price: float
    vwap: float
    volume: float


class CryptoTickerAggregator:
    """High-throughput zero-copy ring buffer aggregator for streaming crypto prices."""

    __slots__ = ("_buffer", "_capacity", "_head", "_size", "symbol")

    def __init__(self, symbol: str, capacity: int = 10000):
        self.symbol = symbol
        self._capacity = capacity
        self._buffer = array.array("d", [0.0] * (capacity * 3))
        self._head = 0
        self._size = 0

    def push(self, price: float, volume: float, timestamp: float | None = None) -> None:
        ts = timestamp or time.time()
        idx = (self._head % self._capacity) * 3
        view = memoryview(self._buffer)
        view[idx : idx + 3] = array.array("d", [ts, price, volume])
        self._head += 1
        if self._size < self._capacity:
            self._size += 1

    def compute_vwap(self, window_seconds: float = 60.0) -> TickerBatch:
        if not self._size:
            return TickerBatch(self.symbol, 0.0, 0.0, 0.0)

        now = time.time()
        cutoff = now - window_seconds
        buf = memoryview(self._buffer)

        total_vol = 0.0
        pv_sum = 0.0
        price_sum = 0.0
        count = 0

        for i in range(self._size):
            pos = ((self._head - 1 - i) % self._capacity) * 3
            ts, price, vol = buf[pos : pos + 3]
            if ts < cutoff:
                break
            total_vol += vol
            pv_sum += price * vol
            price_sum += price
            count += 1

        if count == 0:
            return TickerBatch(self.symbol, 0.0, 0.0, 0.0)

        avg_price = price_sum / count
        vwap = (pv_sum / total_vol) if total_vol > 0 else avg_price
        return TickerBatch(self.symbol, avg_price, vwap, total_vol)


def process_ticks(ticks: list[tuple[str, float, float]]) -> Iterator[TickerBatch]:
    aggregators: dict[str, CryptoTickerAggregator] = {}
    for symbol, price, volume in ticks:
        if symbol not in aggregators:
            aggregators[symbol] = CryptoTickerAggregator(symbol)
        agg = aggregators[symbol]
        agg.push(price, volume)
        yield agg.compute_vwap(30.0)
