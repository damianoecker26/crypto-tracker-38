import hashlib
from decimal import Decimal
from typing import Any, Dict

def hash_payload(data: Dict[str, Any]) -> str:
    return hashlib.sha256(str(sorted(data.items())).encode()).hexdigest()

def normalize_crypto(value: Any) -> Decimal:
    try:
        return Decimal(str(value)).normalize()
    except Exception:
        return Decimal('0')

class DataSynthesizer:
    def __init__(self, raw_stream: list):
        self.stream = raw_stream

    def collapse(self, key: str) -> Decimal:
        total = sum(normalize_crypto(item.get(key, 0)) for item in self.stream)
        return total

def format_currency(amount: Decimal, symbol: str = '$') -> str:
    return f"{symbol}{amount:,.8f}".rstrip('0').rstrip('.')

def validate_ticker(ticker: str) -> bool:
    return bool(ticker and ticker.isalnum() and len(ticker) <= 10)

def sanitize_exchange_data(data: Dict) -> Dict:
    return {k.lower(): v for k, v in data.items() if v is not None}