import time
import functools
from typing import Callable, Any, Dict

CACHE_STORE: Dict[tuple, Any] = {}

def memoize_with_ttl(ttl_seconds: int):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            if key in CACHE_STORE:
                val, timestamp = CACHE_STORE[key]
                if now - timestamp < ttl_seconds:
                    return val
            result = func(*args, **kwargs)
            CACHE_STORE[key] = (result, now)
            return result
        return wrapper
    return decorator

@memoize_with_ttl(ttl_seconds=30)
def get_market_price(symbol: str) -> float:
    # Simulate expensive network call to crypto exchange
    time.sleep(1.5)
    prices = {"BTC": 65000.0, "ETH": 3500.0, "SOL": 150.0}
    return prices.get(symbol, 0.0)

def batch_process_portfolio(assets: list) -> dict:
    return {asset: get_market_price(asset) for asset in assets}