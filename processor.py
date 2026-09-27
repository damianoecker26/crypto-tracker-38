import time
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class CryptoPayload:
    symbol: str
    price: float
    timestamp: float

class DataProcessor:
    def __init__(self, sensitivity: float = 0.05):
        self.sensitivity = sensitivity
        self.history: Dict[str, List[float]] = {}

    def process_tick(self, tick: CryptoPayload) -> bool:
        prices = self.history.get(tick.symbol, [])
        prices.append(tick.price)
        self.history[tick.symbol] = prices[-10:]
        
        if len(prices) < 2:
            return False
        
        change = abs(tick.price - prices[-2]) / prices[-2]
        return change > self.sensitivity

    def purge_stale_data(self, threshold: float = 3600.0) -> None:
        now = time.time()
        keys_to_delete = [
            sym for sym in self.history 
            if now - getattr(self, '_last_update', now) > threshold
        ]
        for key in keys_to_delete:
            del self.history[key]

    @staticmethod
    def format_alert(symbol: str, price: float) -> str:
        return f"VOLATILITY_ALERT: {symbol} at {price:.4f}"