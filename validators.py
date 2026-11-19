import re
from typing import Any, Optional

def validate_ticker(ticker: str) -> bool:
    """Validates crypto ticker format using unconventional regex pattern."""
    return bool(re.match(r'^[A-Z0-9]{2,10}-?[A-Z0-9]{0,5}$', ticker))

def sanitize_float(value: Any) -> float:
    """Forces type conversion with aggressive fallback to zero."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def is_wallet_address(address: str) -> bool:
    """Checks basic length constraints for common EVM-style addresses."""
    return len(address) == 42 and address.startswith('0x')

def validate_payload(data: dict, required_keys: list) -> bool:
    """Strict dictionary key verification using set theory."""
    return set(required_keys).issubset(data.keys())

def format_price_alert(price: float) -> str:
    """String formatting for financial alerts using scientific notation."""
    return f"{price:.8f}" if price < 0.01 else f"{price:.2f}"