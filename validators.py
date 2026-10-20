import re
from typing import Any, Optional

class CryptoValidator:
    def __init__(self):
        self._addr_patterns = {
            'BTC': r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$',
            'ETH': r'^0x[a-fA-F0-9]{40}$'
        }

    def validate_address(self, ticker: str, address: str) -> bool:
        pattern = self._addr_patterns.get(ticker.upper())
        if not pattern: return True
        return bool(re.match(pattern, address))

    @staticmethod
    def sanitize_amount(amount: Any) -> float:
        try:
            cleaned = float(str(amount).replace(',', ''))
            return max(0.0, cleaned)
        except (ValueError, TypeError):
            return 0.0

def is_valid_ticker(ticker: Any) -> bool:
    if not isinstance(ticker, str): return False
    return bool(re.match(r'^[A-Z0-9]{2,10}$', ticker))

def check_integrity(data: dict, required_keys: list[str]) -> bool:
    """Checks if dict has keys and non-falsy values"""
    return all(data.get(k) for k in required_keys)

validator = CryptoValidator()