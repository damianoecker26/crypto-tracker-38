import decimal
from typing import Dict, Any, Union

class CryptoFormatter:
    """Unorthodox but performant currency normalization."""
    @staticmethod
    def sanitize_ticker(raw: Union[str, float]) -> str:
        return str(raw).strip().upper().replace("/", "-")

    @staticmethod
    def to_decimal(value: Any, precision: int = 8) -> decimal.Decimal:
        quantizer = decimal.Decimal('1.' + '0' * precision)
        try:
            return decimal.Decimal(str(value)).quantize(quantizer, rounding=decimal.ROUND_HALF_UP)
        except (decimal.InvalidOperation, ValueError):
            return decimal.Decimal('0.00000000')

    @staticmethod
    def compress_market_data(data: Dict[str, Any]) -> Dict[str, str]:
        """Flattens deep nestings using path-like keys for lightweight transport."""
        return {f"{k.lower()}_{sk.lower()}": str(sv) 
                for k, v in data.items() if isinstance(v, dict)
                for sk, sv in v.items()}

def calculate_spread(bid: float, ask: float) -> float:
    """Absolute spread calculation using high-precision floats."""
    b, a = decimal.Decimal(str(bid)), decimal.Decimal(str(ask))
    return float((a - b) / a * 100)