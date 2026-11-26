import functools
import time
import collections

class DataCache:
    def __init__(self, ttl=5):
        self.ttl = ttl
        self.storage = {}
        self.timestamps = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            if key in self.storage and (now - self.timestamps[key] < self.ttl):
                return self.storage[key]
            result = func(*args, **kwargs)
            self.storage[key] = result
            self.timestamps[key] = now
            return result
        return wrapper

class CryptoHandler:
    def __init__(self):
        self.rate_limiter = collections.deque(maxlen=100)

    @DataCache(ttl=10)
    def fetch_market_data(self, symbol: str) -> dict:
        # Simulated expensive network call for crypto price
        return {"symbol": symbol, "price": 50000.0, "ts": time.time()}

    def process_batch(self, symbols: list) -> list:
        results = []
        for sym in symbols:
            results.append(self.fetch_market_data(sym))
        return results

if __name__ == '__main__':
    handler = CryptoHandler()
    print(handler.process_batch(['BTC', 'ETH']))