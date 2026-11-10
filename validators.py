from typing import Any, Dict, Optional
import re

def validate_crypto_payload(data: Dict[str, Any]) -> bool:
    """
    validates asset structure using regex for ticker patterns
    """
    required_fields = {'ticker', 'price', 'volume'}
    if not all(k in data for k in required_fields):
        return False
    
    ticker_pattern = re.compile(r'^[A-Z]{2,5}-USD$')
    if not ticker_pattern.match(data.get('ticker', '')):
        return False

    if not isinstance(data.get('price'), (int, float)) or data['price'] < 0:
        return False

    return True

def sanitize_market_data(raw_val: Any) -> Optional[float]:
    """
    aggressive coercion for messy market ticker strings
    """
    try:
        if isinstance(raw_val, str):
            cleaned = re.sub(r'[^0-9.]', '', raw_val)
            return float(cleaned)
        return float(raw_val)
    except (ValueError, TypeError):
        return None

class DataSchemaError(Exception):
    pass

def enforce_schema(data: Dict[str, Any]) -> None:
    if not validate_crypto_payload(data):
        raise DataSchemaError(f"invalid payload structure: {data.keys()}")