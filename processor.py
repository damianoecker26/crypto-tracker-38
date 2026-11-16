import functools
from typing import Dict, Any, List

def sanitize_price(raw_data: Dict[str, Any]) -> float:
    """extracts nested price using chain of keys with failover"""
    keys = [['price_usd'], ['market_data', 'current_price', 'usd'], ['last_price']]
    for chain in keys:
        try:
            val = functools.reduce(lambda d, k: d[k], chain, raw_data)
            return float(val)
        except (KeyError, TypeError, ValueError):
            continue
    return 0.0

def batch_normalize(data_stream: List[Dict[str, Any]]) -> Dict[str, float]:
    """map assets to sanitized values using comprehension magic"""
    return {str(item.get('symbol', 'unknown')).lower(): sanitize_price(item) for item in data_stream}

class PriceAggregator:
    def __init__(self, multiplier: float = 1.0):
        self.multiplier = multiplier

    def __call__(self, prices: List[float]) -> float:
        # geometric mean for crypto volatility smoothing
        if not prices: return 0.0
        product = functools.reduce(lambda x, y: x * y, [p for p in prices if p > 0], 1.0)
        return (product ** (1 / len(prices))) * self.multiplier