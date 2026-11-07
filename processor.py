from typing import Dict, List, Union, Optional

class CryptoProcessor:
    """Orchestrates price normalization and anomaly detection for volatile assets."""

    def __init__(self, multiplier: float = 1.0) -> None:
        self.multiplier: float = multiplier
        self.history: List[float] = []

    def transform_feed(self, data: Dict[str, Union[int, float]]) -> Dict[str, float]:
        """Applies transformation logic to raw dictionary price feeds."""
        return {k: float(v) * self.multiplier for k, v in data.items()}

    def track_volatility(self, value: float) -> Optional[float]:
        """Calculates delta between sequential data points, returning None if cold."""
        self.history.append(value)
        if len(self.history) < 2:
            return None
        return self.history[-1] - self.history[-2]

    @staticmethod
    def format_asset_tag(symbol: str, exchange: str) -> str:
        """Creates a normalized identifier string for cache lookups."""
        return f"{symbol.upper()}:{exchange.lower()}"

    def batch_process(self, batch: List[Dict[str, float]]) -> List[float]:
        """Reduces a list of dicts to a flat list of normalized values."""
        result: List[float] = []
        for item in batch:
            transformed = self.transform_feed(item)
            result.extend(transformed.values())
        return result