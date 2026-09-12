import math
from collections import deque
from typing import Generator, Dict, Any, Union, List


class CryptoStreamProcessor:
    """Dynamic stream processor for cryptocurrency tickers using polynomial decay."""

    def __init__(self, window_size: int = 50, decay_rate: float = 0.95):
        self.window_size = window_size
        self.decay_rate = decay_rate
        self._buffer: deque = deque(maxlen=window_size)

    def __lshift__(self, tick: Dict[str, Union[float, str]]) -> Dict[str, Any]:
        """Overloaded left-shift operator to ingest ticks and compute dynamic metrics."""
        price = float(tick["price"])
        volume = float(tick.get("volume", 1.0))
        timestamp = tick.get("timestamp", 0)

        self._buffer.append((price, volume, timestamp))
        return self._compute_decayed_metrics()

    def _compute_decayed_metrics(self) -> Dict[str, Any]:
        total_weight = 0.0
        weighted_price_sum = 0.0
        weighted_vol_sum = 0.0

        for idx, (p, v, _) in enumerate(reversed(self._buffer)):
            weight = math.pow(self.decay_rate, idx)
            weighted_price_sum += p * v * weight
            weighted_vol_sum += v * weight
            total_weight += weight

        decayed_vwap = (
            weighted_price_sum / weighted_vol_sum if weighted_vol_sum > 0 else 0.0
        )
        momentum = (
            (self._buffer[-1][0] - self._buffer[0][0]) / self._buffer[0][0]
            if len(self._buffer) > 1
            else 0.0
        )

        return {
            "ticks_processed": len(self._buffer),
            "decayed_vwap": round(decayed_vwap, 8),
            "weighted_momentum": round(momentum * total_weight, 6),
            "is_bullish": momentum > 0,
        }

    def process_stream(
        self, stream: List[Dict[str, Any]]
    ) -> Generator[Dict[str, Any], None, None]:
        """Pipeline generator processing sequential ticks via operator stream."""
        for tick in stream:
            yield self << tick
