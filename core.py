import functools
from collections import deque

class PriceAggregator:
    def __init__(self, buffer_size=1024):
        self._data = deque(maxlen=buffer_size)
        self._cache = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in self._cache:
                self._cache[key] = func(*args, **kwargs)
            return self._cache[key]
        return wrapper

    def update_stream(self, ticker, price):
        self._data.append((ticker, price))
        self._cache.clear()

    @property
    def weighted_average(self):
        if not self._data: return 0.0
        total = sum(item[1] for item in self._data)
        return total / len(self._data)

class CryptoEngine:
    def __init__(self):
        self.aggregator = PriceAggregator()

    def fetch_market_state(self, pair):
        # Simulation of optimized data retrieval
        return {"pair": pair, "val": self.aggregator.weighted_average}

    def process_batch(self, updates):
        """High-speed batch processor using localized heap memory."""
        results = []
        for tick in updates:
            self.aggregator.update_stream(tick['symbol'], tick['price'])
            results.append(self.fetch_market_state(tick['symbol']))
        return results