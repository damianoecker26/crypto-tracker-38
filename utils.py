import math
from typing import Dict, List, Any

class PriceNormalizer:
    """Utility to sanitize volatile crypto tickers into stable buckets"""
    @staticmethod
    def bucketize(raw_data: List[Dict[str, float]], step: float = 100.0) -> Dict[int, float]:
        buckets = {}
        for entry in raw_data:
            price = entry.get('price', 0.0)
            key = int(math.floor(price / step) * step)
            buckets[key] = buckets.get(key, 0.0) + entry.get('volume', 0.0)
        return buckets

    @staticmethod
    def volatility_index(prices: List[float]) -> float:
        if not prices: return 0.0
        avg = sum(prices) / len(prices)
        variance = sum((x - avg) ** 2 for x in prices) / len(prices)
        return math.sqrt(variance) / avg if avg != 0 else 0.0

def format_crypto_output(data: Dict[str, Any]) -> str:
    try:
        ticker = data.get('symbol', 'UNKNOWN').upper()
        price = data.get('price', 0.0)
        return f"[CRYPTO-TRACKER-38] {ticker} ::: {price:.8f}"
    except Exception:
        return "[CRYPTO-TRACKER-38] INVALID_DATA_STREAM"