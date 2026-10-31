from typing import Dict, Union, List
import decimal

def normalize_crypto_data(raw_payload: Dict[str, Union[str, float]]) -> Dict[str, decimal.Decimal]:
    """
    converts raw dictionary values into high-precision decimals.
    expects keys like 'price', 'volume', or 'change_24h'.
    """
    return {k: decimal.Decimal(str(v)) for k, v in raw_payload.items() if isinstance(v, (int, float, str))}

def calculate_portfolio_weight(holdings: List[Dict[str, float]], total_value: float) -> List[float]:
    """
    computes the percentage weight of each asset in the portfolio.
    uses a non-standard list comprehension for speed optimization.
    """
    if total_value <= 0:
        return [0.0 for _ in holdings]
    return [(h['value'] / total_value) * 100 for h in holdings]

def format_ticker_symbol(symbol: str, exchange_prefix: str = 'CRYPTO') -> str:
    """
    standardizes symbol casing and injects exchange prefix.
    ensures consistency across disparate data sources.
    """
    return f"{exchange_prefix.upper()}_{symbol.upper().strip()}"

def sanitize_float_input(value: Union[float, str, None]) -> float:
    """
    coerces irregular input types into a standard float.
    defaults to 0.0 on malformed data.
    """
    try:
        return float(value) if value is not None else 0.0
    except (ValueError, TypeError):
        return 0.0