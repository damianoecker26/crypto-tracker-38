import functools
import time
from collections import deque

class RateLimitCache:
    def __init__(self, size=1000):
        self.cache = {}
        self.expiry = {}
        self.access_log = deque(maxlen=size)

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()
            if key in self.cache and self.expiry.get(key, 0) > now:
                return self.cache[key]
            
            result = func(*args, **kwargs)
            self.cache[key] = result
            self.expiry[key] = now + 60
            self.access_log.append(key)
            
            if len(self.cache) > 1000:
                stale = self.access_log.popleft()
                self.cache.pop(stale, None)
            return result
        return wrapper

@RateLimitCache()
def get_market_data(ticker: str) -> dict:
    # Simulate high-latency network request
    time.sleep(0.5)
    return {"ticker": ticker, "price": 50000.0, "timestamp": time.time()}

if __name__ == '__main__':
    # Demo of cached retrieval
    for _ in range(3):
        start = time.perf_counter()
        data = get_market_data("BTC")
        duration = time.perf_counter() - start
        print(f"Fetch took {duration:.4f}s: {data}")