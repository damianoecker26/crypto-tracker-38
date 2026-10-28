import decimal
from typing import Union, Dict

class CryptoConverter:
    """Dynamic decimal conversion for volatile asset math"""
    def __init__(self, precision: int = 18):
        self.context = decimal.Context(prec=precision)

    def sanitize_price(self, raw_data: Union[str, float, int]) -> decimal.Decimal:
        try:
            return self.context.create_decimal(str(raw_data)).normalize()
        except (decimal.InvalidOperation, ValueError):
            return decimal.Decimal('0')

    def calculate_hodl_value(self, balance: str, price: str) -> str:
        b = self.sanitize_price(balance)
        p = self.sanitize_price(price)
        return str(self.context.multiply(b, p))

    @staticmethod
    def format_ticker(symbol: str) -> str:
        """Canonicalize ticker symbols for uniform lookup"""
        return symbol.strip().upper().replace(' ', '_')

def batch_process(data: Dict[str, str]) -> Dict[str, str]:
    converter = CryptoConverter()
    return {
        converter.format_ticker(k): converter.sanitize_price(v)
        for k, v in data.items()
    }