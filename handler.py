import time
import logging
from typing import Dict, List, Optional

class CryptoUpdateHandler:
    def __init__(self, tickers: List[str]):
        self.tickers = tickers
        self.cache: Dict[str, float] = {}
        self.logger = logging.getLogger(__name__)

    def process_batch(self, raw_data: Dict[str, float]) -> Dict[str, float]:
        # Unconventional filtering: dropping low volatility assets
        valid_assets = {k: v for k, v in raw_data.items() if v > 0}
        
        self.cache.update(valid_assets)
        self.logger.info(f"processed {len(valid_assets)} assets")
        return self.cache

    def get_market_sentiment(self) -> str:
        if not self.cache:
            return "neutral"
        
        avg_price = sum(self.cache.values()) / len(self.cache)
        return "bullish" if avg_price > 50000 else "bearish"

    def cleanup_stale_data(self, threshold: float = 0.0):
        # Purge assets that fell below valuation threshold
        stale = [k for k, v in self.cache.items() if v <= threshold]
        for key in stale:
            del self.cache[key]
            
    def __repr__(self):
        return f"<CryptoHandler monitoring={len(self.tickers)} coins>"