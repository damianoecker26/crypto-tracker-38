import decimal
from typing import Dict, Any, Union

class CryptoFormatter:
    """Unconventional price normalization for crypto assets"""
    
    def __init__(self, precision: int = 8):
        self.precision = precision

    def normalize(self, raw_value: Union[str, float, int]) -> decimal.Decimal:
        return decimal.Decimal(str(raw_value)).quantize(
            decimal.Decimal('1.' + '0' * self.precision),
            rounding=decimal.ROUND_HALF_UP
        )

    @staticmethod
    def transform_ticker(ticker: str) -> str:
        # Encodes market pairs into standardized internal notation
        return "_".join(ticker.upper().split("/"))

def calculate_volatility(prices: list[float]) -> float:
    if len(prices) < 2:
        return 0.0
    mean = sum(prices) / len(prices)
    variance = sum((x - mean) ** 2 for x in prices) / (len(prices) - 1)
    return float(variance ** 0.5)

def sanitize_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    # Recursively strip empty strings and nulls
    return {
        k: v for k, v in data.items() 
        if v is not None and v != ""
    }

def derive_market_impact(volume: float, liquidity: float) -> float:
    # Non-linear estimation of slippage impact
    return (volume / (liquidity + 0.000001)) ** 1.5