import decimal
from functools import wraps
from typing import Any, Callable, TypeVar

T = TypeVar('T')

def quantize_price(amount: float, precision: int = 8) -> decimal.Decimal:
    """Converts float to precise decimal for crypto math."""
    d_amount = decimal.Decimal(str(amount))
    exponent = decimal.Decimal(10) ** -precision
    return d_amount.quantize(exponent, rounding=decimal.ROUND_HALF_UP)

def retry_on_failure(attempts: int = 3) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for resilient network calls."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_err = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
            raise last_err
        return wrapper
    return decorator

def format_ticker(symbol: str) -> str:
    """Standardizes ticker symbols to uppercase pairs."""
    clean = symbol.upper().replace('/', '').strip()
    return f"{clean[:-3]}/{clean[-3:]}" if len(clean) > 3 else clean

def calculate_percentage_change(old: float, new: float) -> float:
    """Calculates growth factor with safety checks."""
    if not old:
        return 0.0
    return ((new - old) / old) * 100