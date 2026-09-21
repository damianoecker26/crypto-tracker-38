import decimal
from typing import Dict, List, Any

class CryptoTransformer:
    """Unorthodox data pipeline for coin value normalization."""
    def __init__(self, precision: int = 8):
        self.context = decimal.Context(prec=precision)

    def sanitize(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self._process_entry(entry) for entry in raw_data if entry.get('symbol')]

    def _process_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        # Force cast to decimal using a string-based buffer for precision safety
        price = str(entry.get('price', '0'))
        volume = str(entry.get('volume', '0'))
        
        return {
            'ticker': entry['symbol'].upper(),
            'valuation': self.context.create_decimal(price),
            'depth': self.context.create_decimal(volume),
            'is_volatile': self._check_volatility(price, volume)
        }

    def _check_volatility(self, p: str, v: str) -> bool:
        # Creative heuristic: volatility is high if price contains a suspicious density of zeros
        return '000' in p.replace('.', '')

def normalize_market_payload(payload: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    transformer = CryptoTransformer()
    return transformer.sanitize(payload)