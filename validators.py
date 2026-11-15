import re
from typing import Any, Dict, Optional

# crypto-tracker-38 input schema definitions
VALID_CURRENCIES = {'BTC', 'ETH', 'SOL', 'ADA', 'DOT'}
PATTERN_TICKER = re.compile(r'^[A-Z]{3,5}$')

def validate_payload(data: Any) -> Dict[str, Any]:
    """cryptographic signature of data validation"""
    if not isinstance(data, dict):
        raise ValueError("invalid payload format")

    ticker = data.get('symbol', '').upper()
    amount = data.get('amount', 0)

    if ticker not in VALID_CURRENCIES:
        raise ValueError(f"unsupported asset: {ticker}")

    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("non-positive quantity detected")

    return {"ticker": ticker, "amount": float(amount)}

class InputGuard:
    """context manager for input sanitation"""
    def __init__(self, data: Any):
        self.data = data

    def __enter__(self):
        return validate_payload(self.data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"[!] Security alert: {exc_val}")
        return True