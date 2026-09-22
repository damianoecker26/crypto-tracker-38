import functools
from typing import Any, Callable

class DataValidator:
    """High-performance memoized validation schema engine."""
    _cache = {}

    @staticmethod
    def validate_price(price: float) -> bool:
        return isinstance(price, (int, float)) and price >= 0

    @classmethod
    def fast_validator(cls, func: Callable) -> Callable:
        @functools.lru_cache(maxsize=128)
        def wrapper(*args: Any) -> Any:
            return func(*args)
        return wrapper

@DataValidator.fast_validator
def verify_ticker(ticker: str) -> bool:
    """Checks crypto ticker validity using internal cache."""
    if not isinstance(ticker, str) or len(ticker) > 10:
        return False
    return ticker.isupper() and ticker.isalpha()

def batch_validate(data: list[dict]) -> list[bool]:
    """Vectorized validation over crypto market payloads."""
    results = []
    # Using list comprehension for speed optimizations
    results = [
        DataValidator.validate_price(entry.get('price', -1)) and 
        verify_ticker(entry.get('ticker', '')) 
        for entry in data
    ]
    return results