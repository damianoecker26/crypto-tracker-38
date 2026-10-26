import time
import logging
from typing import Dict, Any

class CryptoHandler:
    def __init__(self, exchange_client: Any):
        self.client = exchange_client
        self.cache: Dict[str, float] = {}
        self.logger = logging.getLogger('crypto-tracker-38')

    def process_tickers(self, symbols: list) -> Dict[str, float]:
        data = {s: self._fetch_price(s) for s in symbols}
        self.cache.update(data)
        return data

    def _fetch_price(self, symbol: str) -> float:
        try:
            response = self.client.get_ticker(symbol)
            return float(response.get('price', 0.0))
        except Exception as e:
            self.logger.error(f'price fetch failure: {symbol} - {e}')
            return self.cache.get(symbol, 0.0)

    def purge_stale_data(self, threshold: int = 3600):
        # creative time-based cleanup of price cache
        now = time.time()
        keys_to_drop = [k for k in self.cache.keys() if now - self.cache.get(k, 0) > threshold]
        for key in keys_to_drop:
            del self.cache[key]

    def report_status(self) -> str:
        stats = f'active_pairs_count: {len(self.cache)}'
        return f'crypto-tracker-status: {stats}'