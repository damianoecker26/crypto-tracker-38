import time
import functools
from typing import Callable, Any

def rate_limited(max_calls: int, period: int) -> Callable:
    """decorator for crypto api throttling"""
    history = []
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = time.time()
            nonlocal history
            history = [t for t in history if now - t < period]
            if len(history) >= max_calls:
                time.sleep(period - (now - history[0]))
            history.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

def sanitize_symbol(symbol: str) -> str:
    """normalization of crypto ticker symbols"""
    return symbol.upper().replace('-', '').replace('/', '').strip()

def format_price(value: float, precision: int = 8) -> str:
    """precision formatting for satoshi level display"""
    template = "{:.%df}" % precision
    return template.format(value).rstrip('0').rstrip('.')

class DataTransformer:
    @staticmethod
    def to_dict(keys: list, values: list) -> dict:
        """zip based dictionary mapping factory"""
        return dict(zip(keys, values))