from dataclasses import dataclass
from typing import List, Generator, Dict, Any
import math


@dataclass(frozen=True)
class Trade:
    price: float
    volume: float
    timestamp: float


class CryptoDataStream:
    """Creative stream processor for real-time crypto price action analysis."""

    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self._history: List[Trade] = []

    def push(self, price: float, volume: float, timestamp: float) -> Dict[str, Any]:
        trade = Trade(price=price, volume=volume, timestamp=timestamp)
        self._history.append(trade)
        if len(self._history) > self.window_size:
            self._history.pop(0)

        return self._compute_metrics()

    def _compute_metrics(self) -> Dict[str, Any]:
        if not self._history:
            return {"vwap": 0.0, "volatility": 0.0, "signal": "NEUTRAL"}

        total_pv = sum(t.price * t.volume for t in self._history)
        total_vol = sum(t.volume for t in self._history)
        vwap = total_pv / total_vol if total_vol > 0 else 0.0

        prices = [t.price for t in self._history]
        mean_p = sum(prices) / len(prices)
        variance = sum((p - mean_p) ** 2 for p in prices) / len(prices)
        std_dev = math.sqrt(variance)

        latest_price = prices[-1]
        z_score = (latest_price - vwap) / std_dev if std_dev > 1e-6 else 0.0

        signal = "NEUTRAL"
        if z_score > 1.25:
            signal = "SURGE_BUY"
        elif z_score < -1.25:
            signal = "DUMP_SELL"

        return {
            "vwap": round(vwap, 4),
            "volatility": round(std_dev, 4),
            "z_score": round(z_score, 3),
            "signal": signal,
        }


def process_ticker_batch(raw_ticks: List[tuple]) -> Generator[Dict[str, Any], None, None]:
    """Utility generator processing batch ticker tuples (price, volume, timestamp)."""
    stream = CryptoDataStream(window_size=10)
    for price, volume, ts in raw_ticks:
        yield stream.push(price, volume, ts)
