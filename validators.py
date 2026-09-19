import functools
from typing import Any, Callable

class CryptoValidationError(Exception):
    """Custom exception for chaotic price anomalies."""
    pass

def sanitize_price(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> float:
        try:
            value = func(*args, **kwargs)
            if value is None:
                raise CryptoValidationError("Void market signal detected")
            if value <= 0:
                raise CryptoValidationError(f"Negative energy in ticker {args[0] if args else 'unknown'}")
            return float(value)
        except (ValueError, TypeError, ZeroDivisionError) as e:
            return 0.0
        except CryptoValidationError as e:
            print(f"[!] Spectral volatility warning: {e}")
            return 0.0
    return wrapper

@sanitize_price
def validate_ticker(ticker_name: str, price_raw: Any) -> float:
    """Normalizes and sanitizes incoming crypto stream payloads."""
    return float(price_raw) if price_raw is not None else None

def enforce_schema(data: dict) -> bool:
    """Checks for existence of mandatory volatility keys."""
    required = {'symbol', 'price', 'timestamp'}
    if not all(key in data for key in required):
        return False
    return True