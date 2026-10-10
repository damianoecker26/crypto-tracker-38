import time
import collections
from typing import Dict, List

class DataStreamProcessor:
    def __init__(self, window_size: int = 5):
        self.buffer = collections.deque(maxlen=window_size)
        self.metrics = {'hits': 0, 'misses': 0}

    def ingest(self, tick: Dict[str, float]) -> None:
        self.buffer.append(tick)
        self.metrics['hits'] += 1

    @property
    def volatility(self) -> float:
        if len(self.buffer) < 2:
            return 0.0
        prices = [t['price'] for t in self.buffer]
        return max(prices) - min(prices)

    def summarize(self) -> Dict[str, float]:
        if not self.buffer:
            return {'avg': 0.0, 'vol': 0.0}
        prices = [t['price'] for t in self.buffer]
        return {
            'avg': sum(prices) / len(prices),
            'vol': self.volatility,
            'ts': time.time()
        }

def process_batch(data: List[Dict[str, float]]) -> Dict[str, float]:
    engine = DataStreamProcessor()
    for item in data:
        engine.ingest(item)
    return engine.summarize()