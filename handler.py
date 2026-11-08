from typing import Dict, Any, Optional
import logging

class CryptoHandler:
    """Orchestrates market data flow for crypto-tracker-38."""

    def __init__(self, ticker_map: Dict[str, str]) -> None:
        self.ticker_map: Dict[str, str] = ticker_map
        self.logger = logging.getLogger(__name__)

    def resolve_asset(self, symbol: str) -> Optional[str]:
        """Map internal tickers to global exchange identifiers."""
        return self.ticker_map.get(symbol.upper())

    def process_payload(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Extract and sanitize pricing data from raw network blobs."""
        results: Dict[str, float] = {}
        for key, value in data.items():
            asset = self.resolve_asset(key)
            if asset:
                try:
                    results[asset] = float(value)
                except (ValueError, TypeError) as e:
                    self.logger.warning(f"Skipping malformed data for {asset}: {e}")
        return results

    def __repr__(self) -> str:
        """Return string representation of current handler state."""
        return f"CryptoHandler(tracked_assets={len(self.ticker_map)})"