from collections import deque
from typing import Dict, Generator, List, Union, Any
import math

class CryptoStreamProcessor:
    """
    Stateful generator pipeline for processing high-frequency crypto trade ticks
    and computing real-time VWAP and adaptive anomaly thresholds.
    """
    def __init__(self, window_size: int = 50, z_threshold: float = 2.5):
        self.window_size = window_size
        self.z_threshold = z_threshold
        self._history = deque(maxlen=window_size)
        
    def aggregate_ticks(self, raw_ticks: List[Dict[str, Any]]) -> Generator[Dict[str, Union[float, bool, str, int]], None, None]:
        """
        Consumes raw ticker data (price, volume, timestamp) and yields calculated stats.
        """
        for tick in raw_ticks:
            price = float(tick.get("price", 0.0))
            volume = float(tick.get("volume", 0.0))
            symbol = str(tick.get("symbol", "UNKNOWN")).upper()
            
            if price <= 0 or volume <= 0:
                continue
                
            self._history.append((price, volume))
            total_vol = sum(v for _, v in self._history)
            vwap = sum(p * v for p, v in self._history) / total_vol if total_vol > 0 else price
            
            prices = [p for p, _ in self._history]
            mean_p = sum(prices) / len(prices)
            variance = sum((p - mean_p) ** 2 for p in prices) / len(prices)
            std_dev = math.sqrt(variance) if variance > 0 else 1e-9
            
            z_score = (price - mean_p) / std_dev
            is_anomaly = abs(z_score) >= self.z_threshold
            
            yield {
                "symbol": symbol,
                "price": price,
                "vwap": round(vwap, 8),
                "z_score": round(z_score, 4),
                "is_volume_anomaly": is_anomaly,
                "window_depth": len(self._history)
            }

def process_trade_feed(ticks: List[Dict[str, Any]], window: int = 30) -> Dict[str, Any]:
    """Helper wrapper function to execute tick processing pipeline and extract summaries."""
    processor = CryptoStreamProcessor(window_size=window)
    processed = list(processor.aggregate_ticks(ticks))
    anomalies = [t for t in processed if t["is_volume_anomaly"]]
    
    return {
        "processed_count": len(processed),
        "anomaly_count": len(anomalies),
        "last_vwap": processed[-1]["vwap"] if processed else 0.0,
        "feed": processed
    }
