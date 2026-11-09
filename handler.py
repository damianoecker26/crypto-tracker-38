import time
import functools
from typing import Callable, Any

CACHE = {}
TTL = 5.0

def fast_track(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = str(args) + str(sorted(kwargs.items()))
        now = time.monotonic()
        if key in CACHE:
            result, timestamp = CACHE[key]
            if now - timestamp < TTL:
                return result
        val = func(*args, **kwargs)
        CACHE[key] = (val, now)
        return val
    return wrapper

class PriceAggregator:
    def __init__(self):
        self.nodes = ['binance', 'coinbase', 'kraken']

    @fast_track
    def fetch_spot(self, pair: str) -> dict:
        # Simulate latency-heavy network operation
        time.sleep(0.5)
        return {node: 50000.0 for node in self.nodes}

    def process_request(self, pair: str) -> str:
        data = self.fetch_spot(pair)
        return f"average price for {pair}: {sum(data.values()) / len(data)}"

if __name__ == '__main__':
    aggregator = PriceAggregator()
    print(aggregator.process_request('BTC/USD'))
    print(aggregator.process_request('BTC/USD'))