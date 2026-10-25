from collections import deque
from dataclasses import dataclass
from typing import Generator, Iterable, Dict, Any

@dataclass(frozen=True)
class CryptoTick:
    symbol: str
    price: float
    volume: float
    timestamp: float

class RollingVWAPEngine:
    """Dynamic sliding-window VWAP and volatility anomaly calculator using generator pipelines."""

    def __init__(self, window_size: int = 50, anomaly_threshold: float = 2.5):
        self.window_size = window_size
        self.anomaly_threshold = anomaly_threshold
        self._history: Dict[str, deque] = {}

    def __call__(self, stream: Iterable[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        for raw in stream:
            tick = CryptoTick(
                symbol=str(raw["symbol"]),
                price=float(raw["price"]),
                volume=float(raw["volume"]),
                timestamp=float(raw["timestamp"])
            )
            
            if tick.symbol not in self._history:
                self._history[tick.symbol] = deque(maxlen=self.window_size)
            
            q = self._history[tick.symbol]
            q.append(tick)

            total_pv = sum(t.price * t.volume for t in q)
            total_vol = sum(t.volume for t in q)
            vwap = total_pv / total_vol if total_vol > 0 else tick.price

            mean_price = sum(t.price for t in q) / len(q)
            variance = sum((t.price - mean_price) ** 2 for t in q) / len(q)
            std_dev = variance ** 0.5

            z_score = (tick.price - mean_price) / std_dev if std_dev > 0 else 0.0
            is_anomaly = abs(z_score) >= self.anomaly_threshold

            yield {
                "symbol": tick.symbol,
                "price": tick.price,
                "vwap": round(vwap, 8),
                "z_score": round(z_score, 4),
                "is_anomaly": is_anomaly,
                "volume_accumulated": round(total_vol, 4)
            }

def process_crypto_stream(raw_ticks: Iterable[Dict[str, Any]], window: int = 30) -> list[Dict[str, Any]]:
    engine = RollingVWAPEngine(window_size=window)
    return list(engine(raw_ticks))
