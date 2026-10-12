import time
import functools
from typing import Callable, Any

def throttle(seconds: int = 5):
    def decorator(func: Callable):
        last_called = 0
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_called
            elapsed = time.time() - last_called
            if elapsed < seconds:
                return None
            last_called = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def format_currency(value: float, symbol: str = '$') -> str:
    return f"{symbol}{value:,.2f}"

class DataSanitizer:
    @staticmethod
    def strip_keys(data: dict, keys: list) -> dict:
        return {k: v for k, v in data.items() if k not in keys}

def retry_request(attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == attempts - 1: raise e
                    time.sleep(delay)
        return wrapper
    return decorator