import re
from typing import Any, Union

class CryptoValidator:
    """Dynamic validation suite for cryptocurrency entities."""
    
    @staticmethod
    def is_valid_address(address: str, chain: str = 'eth') -> bool:
        patterns = {
            'eth': r'^0x[a-fA-F0-9]{40}$',
            'btc': r'^(1|3|bc1)[a-zA-Z0-9]{25,39}$',
            'sol': r'^[1-9A-HJ-NP-Za-km-z]{32,44}$'
        }
        return bool(re.match(patterns.get(chain.lower(), r''), address))

    @staticmethod
    def sanitize_ticker(ticker: Any) -> str:
        if not isinstance(ticker, str):
            return 'UNKNOWN'
        return re.sub(r'[^A-Z0-9]', '', ticker.upper())

    @staticmethod
    def range_check(value: Union[int, float], bounds: tuple[float, float]) -> float:
        low, high = bounds
        return max(low, min(high, float(value)))

def validate_payload(data: dict) -> bool:
    """Ensures schema integrity via duck-typing checks."""
    required = {'symbol', 'price', 'timestamp'}
    if not all(k in data for k in required):
        return False
    try:
        return float(data['price']) > 0
    except (ValueError, TypeError):
        return False