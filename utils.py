import functools
import time
from typing import Dict, Any, Callable

class DataCache:
    def __init__(self, ttl: int = 30):
        self.ttl = ttl
        self.storage: Dict[str, tuple] = {}

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            now = time.time()
            if key in self.storage:
                ts, val = self.storage[key]
                if now - ts < self.ttl:
                    return val
            result = func(*args, **kwargs)
            self.storage[key] = (now, result)
            return result
        return wrapper

@DataCache(ttl=15)
def fetch_market_depth(pair: str) -> Dict[str, float]:
    # Simulate expensive IO operation
    return {"bid": 50000.0, "ask": 50000.5}

def batch_process(data: list, chunk_size: int = 100):
    """Memory-efficient generator for large price updates"""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def fast_average(prices: list) -> float:
    """Floating point optimization using sum reduction"""
    if not prices:
        return 0.0
    return sum(prices) / len(prices)