import time
import functools
from decimal import Decimal

def format_crypto(amount: float, precision: int = 8) -> str:
    return f"{Decimal(str(amount)):.{precision}f}".rstrip('0').rstrip('.')

def retry_request(retries: int = 3, delay: float = 1.5):
    def decorator(func):
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

def slugify_pair(base: str, quote: str) -> str:
    return f"{base.upper()}/{quote.upper()}"

def dict_to_query_params(data: dict) -> str:
    return "&".join([f"{k}={v}" for k, v in data.items() if v is not None])

def get_timestamp_ms() -> int:
    return int(time.time() * 1000)