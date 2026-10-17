from typing import Dict, List, Union, Optional

class CryptoProcessor:
    """Orchestrates normalization of ticker data from various exchanges."""

    def __init__(self, multiplier: float = 1.0) -> None:
        self.multiplier: float = multiplier
        self.cache: Dict[str, float] = {}

    def transform(self, raw_data: List[Dict[str, Union[str, float]]]) -> Dict[str, float]:
        """Converts raw API dictionaries into standardized internal float mapping."""
        results: Dict[str, float] = {}
        for entry in raw_data:
            ticker: str = str(entry.get('symbol', 'UNKNOWN')).upper()
            price: float = float(entry.get('price', 0.0))
            results[ticker] = price * self.multiplier
        self.cache.update(results)
        return results

    def get_market_delta(self, ticker: str, current_price: float) -> Optional[float]:
        """Calculates variance between cached price and current market state."""
        previous: Optional[float] = self.cache.get(ticker.upper())
        if previous is None:
            return None
        return (current_price - previous) / previous

def sanitize_stream(data: List[Dict]) -> List[Dict]:
    """Filter out entries with zeroed price signals."""
    return [d for d in data if d.get('price', 0) > 0]
