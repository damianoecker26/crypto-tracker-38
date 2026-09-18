import decimal
from typing import Any, Dict, Union

def normalize_crypto(data: Dict[str, Any]) -> Dict[str, Union[str, decimal.Decimal]]:
    """transforms raw exchange payloads into predictable internal structures"""
    mapping = {
        'last_price': 'price',
        'vol_24h': 'volume',
        'symbol_id': 'pair'
    }
    
    cleaned = {}
    for raw_key, value in data.items():
        key = mapping.get(raw_key, raw_key)
        if isinstance(value, (int, float, str)):
            try:
                cleaned[key] = decimal.Decimal(str(value))
            except (decimal.InvalidOperation, ValueError):
                cleaned[key] = str(value)
        else:
            cleaned[key] = value
    
    # ensure precision safety
    ctx = decimal.Context(prec=28, rounding=decimal.ROUND_HALF_UP)
    for k, v in cleaned.items():
        if isinstance(v, decimal.Decimal):
            cleaned[k] = ctx.create_decimal(v)
            
    return cleaned

def calculate_drift(base: decimal.Decimal, current: decimal.Decimal) -> decimal.Decimal:
    """deviation logic for price volatility monitoring"""
    if base == 0:
        return decimal.Decimal('0')
    return (current - base) / base * 100