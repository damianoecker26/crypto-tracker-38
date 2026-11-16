import time
import functools
from typing import Callable, Any

def retry_on_failure(retries: int = 3, delay: float = 1.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def format_crypto_amount(amount: float, precision: int = 8) -> str:
    return f"{amount:.{precision}f}".rstrip('0').rstrip('.')

def calculate_percent_change(old: float, new: float) -> float:
    if old == 0:
        return 0.0
    return ((new - old) / abs(old)) * 100

def sanitize_ticker(ticker: str) -> str:
    return ''.join(filter(str.isalnum, ticker)).upper()

def timestamp_to_ms(dt_obj) -> int:
    return int(dt_obj.timestamp() * 1000)

def memoize_with_ttl(ttl_seconds: int = 60):
    cache = {}
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args):
            key = str(args)
            now = time.time()
            if key in cache and (now - cache[key]['ts']) < ttl_seconds:
                return cache[key]['val']
            res = func(*args)
            cache[key] = {'val': res, 'ts': now}
            return res
        return wrapper
    return decorator