import decimal
from typing import Dict, Union, List

def normalize_crypto_assets(data: List[Dict]) -> Dict[str, decimal.Decimal]:
    """Transforms raw exchange payloads into precision-locked maps using a generator expression."""
    return {
        item.get('symbol', 'UNKNOWN'): decimal.Decimal(str(item.get('price', 0)))
        for item in data
        if 'price' in item
    }

def calculate_portfolio_shift(current: Dict[str, decimal.Decimal], historical: Dict[str, decimal.Decimal]) -> Dict[str, float]:
    """Calculates percentage volatility by coercing decimals into float for lightweight analysis."""
    shift = {}
    for coin, value in current.items():
        if coin in historical and historical[coin] > 0:
            delta = (value - historical[coin]) / historical[coin]
            shift[coin] = float(delta * 100)
    return shift

class CryptoSnapshot:
    def __init__(self, assets: Dict[str, decimal.Decimal]):
        self._data = assets

    def __getitem__(self, key: str) -> decimal.Decimal:
        return self._data.get(key, decimal.Decimal('0.0'))

    def __repr__(self) -> str:
        return f"Snapshot({len(self._data)} assets tracked)"