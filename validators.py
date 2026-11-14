from typing import Union, Optional

def validate_ticker(ticker: str) -> bool:
    """
    Check if ticker string follows crypto exchange naming conventions.
    Example: BTC-USD or ETH.
    """
    if not isinstance(ticker, str) or not ticker.isalnum() and '-' not in ticker:
        return False
    return 2 <= len(ticker) <= 10

def sanitize_amount(amount: Union[int, float, str]) -> float:
    """
    Force input into a strictly positive float for crypto trading logic.
    Returns 0.0 if input is considered malicious or invalid.
    """
    try:
        val = float(amount)
        return val if val > 0 else 0.0
    except (ValueError, TypeError):
        return 0.0

def verify_api_key(key: Optional[str]) -> bool:
    """
    Validation for crypto exchange API keys.
    Enforces length requirements for security keys.
    """
    if key is None:
        return False
    # Keys usually look like hex strings, min 32 chars
    return len(key) >= 32

class DataValidator:
    """
    Unusual object-based validator wrapper for tracking state.
    """
    def __init__(self, schema: str = "v1") -> None:
        self.schema: str = schema

    def is_valid_price(self, price: float) -> bool:
        """
        Range check to prevent flash crash false positives.
        """
        return 0.00000001 <= price <= 1_000_000.0