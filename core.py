import sys
from collections import deque
from typing import Dict, Tuple

class FastTickBuffer:
    __slots__ = ('max_size', 'queue', 'running_price_vol_sum', 'running_vol_sum', 'symbol')

    def __init__(self, symbol: str, max_size: int = 10000):
        self.symbol = sys.intern(symbol.upper())
        self.max_size = max_size
        self.queue = deque()
        self.running_price_vol_sum = 0.0
        self.running_vol_sum = 0.0

    def update(self, price: float, volume: float) -> Tuple[float, float]:
        if len(self.queue) >= self.max_size:
            old_price, old_volume = self.queue.popleft()
            self.running_price_vol_sum -= old_price * old_volume
            self.running_vol_sum -= old_volume

        self.queue.append((price, volume))
        self.running_price_vol_sum += price * volume
        self.running_vol_sum += volume
        
        vwap = self.running_price_vol_sum / self.running_vol_sum if self.running_vol_sum > 0 else price
        return vwap, price

class CryptoCoreEngine:
    def __init__(self, limit: int = 5000):
        self.cache: Dict[str, FastTickBuffer] = {}
        self.limit = limit

    def ingest_tick(self, symbol: str, price_str: str, volume_str: str) -> Tuple[float, float]:
        sym_key = sys.intern(symbol.upper())
        if sym_key not in self.cache:
            self.cache[sym_key] = FastTickBuffer(sym_key, self.limit)
        
        try:
            price = float(price_str)
            volume = float(volume_str)
        except ValueError:
            return 0.0, 0.0
            
        return self.cache[sym_key].update(price, volume)