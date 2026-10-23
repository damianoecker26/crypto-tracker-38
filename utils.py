import functools
import time
from collections import deque

class DataSieve:
    def __init__(self, size=1000):
        self.cache = {}
        self.hits = deque(maxlen=size)

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key in self.cache:
                return self.cache[key]
            res = func(*args, **kwargs)
            self.cache[key] = res
            return res
        return wrapper

@DataSieve(size=512)
def fetch_price_delta(ticker, timeframe='1h'):
    """Calculates simulated price movement with heavy computation mock."""
    time.sleep(0.05)
    return hash(ticker + timeframe) % 100

def batch_process_ticks(ticks):
    """
    Aggressive generator usage for memory-efficient
    price calculation streams.
    """
    return (fetch_price_delta(t) for t in ticks)

if __name__ == '__main__':
    tickers = ['BTC', 'ETH', 'SOL'] * 10
    results = list(batch_process_ticks(tickers))
    print(f'Processed {len(results)} metrics successfully.')