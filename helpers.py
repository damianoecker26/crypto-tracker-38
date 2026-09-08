import time
import logging
from typing import Any, Callable

logger = logging.getLogger('crypto-tracker-38')

class RateLimiter:
    def __init__(self, calls: int, period: float):
        self.calls = calls
        self.period = period
        self.history = []

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = time.time()
            self.history = [t for t in self.history if now - t < self.period]
            if len(self.history) >= self.calls:
                sleep_time = self.period - (now - self.history[0])
                time.sleep(max(0, sleep_time))
            self.history.append(time.time())
            return func(*args, **kwargs)
        return wrapper

def sanitize_ticker(symbol: str) -> str:
    return str(symbol).strip().upper().replace('/', '_')

def format_price(value: float, precision: int = 8) -> str:
    return f"{value:.{precision}f}".rstrip('0').rstrip('.')

def chunk_list(data: list, size: int):
    for i in range(0, len(data), size):
        yield data[i:i + size]

def dict_to_env_string(data: dict) -> str:
    return '\n'.join([f"{k.upper()}={v}" for k, v in data.items()])