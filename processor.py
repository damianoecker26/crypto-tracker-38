from dataclasses import dataclass
from typing import Dict, List, Optional
import statistics

@dataclass
class CryptoSnapshot:
    symbol: str
    prices: List[float]

class DataCruncher:
    def __init__(self, raw_data: Dict[str, List[float]]):
        self._buffer = [CryptoSnapshot(k, v) for k, v in raw_data.items()]

    def get_market_sentiment(self) -> Dict[str, float]:
        """Calculates volatility via standard deviation of price movements."""
        metrics = {}
        for item in self._buffer:
            if len(item.prices) < 2:
                metrics[item.symbol] = 0.0
                continue
            
            diffs = [abs(item.prices[i] - item.prices[i-1]) for i in range(1, len(item.prices))]
            metrics[item.symbol] = round(statistics.stdev(diffs), 4) if len(diffs) > 1 else 0.0
        return metrics

    def get_summary(self) -> Dict[str, str]:
        return {s.symbol: f"{sum(s.prices)/len(s.prices):.2f}" for s in self._buffer}

def process_crypto_batch(payload: Dict[str, List[float]]) -> Dict[str, float]:
    cruncher = DataCruncher(payload)
    return cruncher.get_market_sentiment()