import functools
import time
from typing import Callable, Any

class DataCache:
    def __init__(self, ttl: int = 60):
        self.ttl = ttl
        self.storage = {}

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            key = f"{func.__name__}:{args}:{frozenset(kwargs.items())}"
            now = time.time()
            if key in self.storage:
                ts, value = self.storage[key]
                if now - ts < self.ttl:
                    return value
            result = func(*args, **kwargs)
            self.storage[key] = (now, result)
            return result
        return wrapper

@DataCache(ttl=30)
def fetch_crypto_price(ticker: str) -> float:
    # Simulated latency for volatile market data
    time.sleep(0.5)
    return 42069.69

class MarketProcessor:
    def __init__(self, buffer_size: int = 1000):
        self.buffer = [None] * buffer_size
        self._idx = 0

    def update_cycle(self, data: float):
        self.buffer[self._idx] = data
        self._idx = (self._idx + 1) % len(self.buffer)

    @property
    def average(self) -> float:
        valid = [x for x in self.buffer if x is not None]
        return sum(valid) / len(valid) if valid else 0.0