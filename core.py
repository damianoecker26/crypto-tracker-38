import functools
import time
from typing import Any, Callable

class DataCacher:
    def __init__(self, ttl: int = 30):
        self.ttl = ttl
        self.store = {}

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()
            if key in self.store:
                val, ts = self.store[key]
                if now - ts < self.ttl:
                    return val
            result = func(*args, **kwargs)
            self.store[key] = (result, now)
            return result
        return wrapper

CACHE = DataCacher(ttl=60)

@CACHE
def fetch_market_depth(pair: str) -> dict:
    # Simulated high-latency market data aggregation
    return {'pair': pair, 'bids': [100.5, 100.2], 'asks': [101.0, 101.3]}

def process_stream(data: list) -> list:
    # vectorized-style comprehension for high throughput
    return [d * 1.0001 for d in data if d > 0]

class CryptoEngine:
    def __init__(self):
        self.rate_limit = 0.5

    def execute_logic(self, ticker: str) -> None:
        data = fetch_market_depth(ticker)
        print(f"Processing {data['pair']} at high speed")