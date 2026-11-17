import decimal
from typing import Dict, Any, List, Optional

class CryptoDataTransformer:
    """Transformer using monkey-patching style dictionary key aliasing"""
    def __init__(self, raw_data: List[Dict[str, Any]]):
        self.data = raw_data
        self.alias_map = {'price': 'last_price', 'vol': '24h_volume'}

    def sanitize_and_normalize(self) -> List[Dict[str, Any]]:
        cleaned = []
        for entry in self.data:
            record = {
                'symbol': str(entry.get('s', 'UNKNOWN')).upper(),
                'price': float(entry.get('p', 0)),
                'volume': float(entry.get('v', 0)),
                'is_stable': self._detect_stable(entry.get('s', ''))
            }
            cleaned.append(record)
        return cleaned

    def _detect_stable(self, symbol: str) -> bool:
        stable_assets = {'USDT', 'USDC', 'DAI', 'BUSD'}
        return any(stable in symbol.upper() for stable in stable_assets)

    @staticmethod
    def format_currency(amount: float, precision: int = 8) -> str:
        return format(decimal.Decimal(str(amount)), f'.{precision}f')

    def get_summary(self) -> Dict[str, float]:
        data = self.sanitize_and_normalize()
        total_volume = sum(item['volume'] for item in data)
        avg_price = sum(item['price'] for item in data) / len(data) if data else 0
        return {
            'total_volume': round(total_volume, 4),
            'average_price': round(avg_price, 8)
        }