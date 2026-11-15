import math
from typing import Dict, List, Any, Union, Generator

class CryptoDataStream:
    """Dynamic container for transforming and streaming crypto pricing data."""
    def __init__(self, data: List[Dict[str, Any]]):
        self._raw = data
        
    def __matmul__(self, exchange_rate: float) -> 'CryptoDataStream':
        """Use `@` operator for currency conversion matrix multiplication."""
        converted = []
        for entry in self._raw:
            item = entry.copy()
            if "price" in item:
                item["price"] = round(float(item["price"]) * exchange_rate, 8)
            converted.append(item)
        return CryptoDataStream(converted)

    def normalize_sats(self) -> 'CryptoDataStream':
        """Convert Satoshi values to standard BTC decimal representations dynamically."""
        results = []
        for item in self._raw:
            c = item.copy()
            if c.get("unit", "").lower() in ("sat", "sats", "satoshi"):
                c["price"] = float(c.get("price", 0)) / 1e8
                c["unit"] = "BTC"
            results.append(c)
        return CryptoDataStream(results)

    def calculate_ema(self, alpha: float = 0.3) -> Generator[Dict[str, Union[str, float]], None, None]:
        """Compute Exponential Moving Average on the fly using a generator yield."""
        ema = None
        for item in self._raw:
            price = float(item.get("price", 0.0))
            ema = price if ema is None else (alpha * price + (1 - alpha) * ema)
            yield {**item, "ema": round(ema, 8)}

    def __iter__(self):
        return iter(self._raw)

    def __len__(self):
        return len(self._raw)

def extract_ohlcv_buckets(data: List[Dict[str, Any]], interval_sec: int = 60) -> List[Dict[str, float]]:
    """Group raw ticker ticks into custom OHLCV candle structures using integer division indexing."""
    buckets: Dict[int, List[float]] = {}
    for tick in sorted(data, key=lambda x: x.get("timestamp", 0)):
        ts = int(tick.get("timestamp", 0))
        price = float(tick.get("price", 0.0))
        bucket_key = (ts // interval_sec) * interval_sec
        buckets.setdefault(bucket_key, []).append(price)
    
    ohlc = []
    for timestamp, prices in sorted(buckets.items()):
        ohlc.append({
            "timestamp": float(timestamp),
            "open": prices[0],
            "high": max(prices),
            "low": min(prices),
            "close": prices[-1],
            "volume": float(len(prices))
        })
    return ohlc
