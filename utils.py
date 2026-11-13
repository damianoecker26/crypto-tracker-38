from typing import Dict, Union, List
import decimal

class CryptoFormatter:
    """Handles eccentric currency representations for crypto-tracker-38."""

    @staticmethod
    def normalize_amount(raw_val: Union[str, float, int]) -> decimal.Decimal:
        """Converts raw input to a high-precision decimal representation."""
        return decimal.Decimal(str(raw_val)).quantize(decimal.Decimal('0.00000001'))

    @staticmethod
    def batch_annotate(data: List[Dict[str, float]]) -> List[Dict[str, decimal.Decimal]]:
        """Transformation of float values into high-precision decimal maps."""
        return [{
            key: CryptoFormatter.normalize_amount(val) 
            for key, val in entry.items()
        } for entry in data]

def format_ticker(symbol: str, price: decimal.Decimal) -> str:
    """String formatting with crypto-specific precision indicators."""
    return f"[{symbol.upper()}] :: {price:f} BTC"

def extract_volatility(history: List[decimal.Decimal]) -> decimal.Decimal:
    """Calculates delta range of asset history for market analysis."""
    if not history:
        return decimal.Decimal('0.0')
    return max(history) - min(history)