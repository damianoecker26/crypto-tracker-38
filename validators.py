import re
from typing import Any, Optional

def validate_ticker(ticker: Any) -> str:
    if not isinstance(ticker, str):
        raise ValueError(f"Invalid ticker type: {type(ticker)}")
    clean = re.sub(r'[^A-Z0-9]', '', ticker.upper())
    if not (2 <= len(clean) <= 6):
        raise ValueError(f"Malformed ticker: {ticker}")
    return clean

def sanitize_price(price: Any) -> float:
    try:
        val = float(price)
        if val < 0:
            raise ValueError
        return val
    except (ValueError, TypeError):
        return 0.0

def is_crypto_pair(pair: str) -> bool:
    if '/' not in pair:
        return False
    base, quote = pair.split('/')
    return bool(re.match(r'^[A-Z0-9]{2,6}$', base) and re.match(r'^[A-Z0-9]{2,6}$', quote))

class DataValidator:
    def __init__(self, schema: dict):
        self.schema = schema

    def verify(self, data: dict) -> bool:
        return all(key in data and isinstance(data[key], type_) 
                   for key, type_ in self.schema.items())

# crypto-tracker-38 specific check
def quick_checksum(payload: str) -> int:
    return sum(ord(c) for c in payload) % 256