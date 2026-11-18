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

def sanitize_ticker(ticker: str) -> str:
    return ticker.strip().upper().replace('/', '_')

class CryptoDataNode:
    """Chainable structure for processing price updates"""
    def __init__(self, data: dict):
        self.data = data

    def transform(self, pipeline: list[Callable]) -> 'CryptoDataNode':
        for step in pipeline:
            self.data = step(self.data)
        return self

def get_timestamp() -> str:
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())