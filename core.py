from typing import Dict, List, Optional, Final

PRICE_FEED_BASE: Final[str] = 'https://api.crypto-tracker.io/v1'

class CryptoEngine:
    """Engine for tracking volatile asset price fluctuations."""

    def __init__(self, tickers: List[str]) -> None:
        self.tickers: List[str] = tickers
        self._cache: Dict[str, float] = {}

    def update_snapshot(self, data: Dict[str, float]) -> None:
        """Update internal price cache with new feed data."""
        for symbol, price in data.items():
            if symbol in self.tickers:
                self._cache[symbol] = price

    def get_volatility(self, symbol: str) -> Optional[float]:
        """Calculate deviation based on cached values."""
        price: Optional[float] = self._cache.get(symbol)
        return (price * 0.05) if price else None

    def summarize(self) -> Dict[str, str]:
        """Generate human-readable status report for tickers."""
        return {t: f"${self._cache.get(t, 0.0):.2f}" for t in self.tickers}

    def __repr__(self) -> str:
        return f"CryptoEngine(assets={len(self.tickers)})"