import time
import decimal
from functools import wraps
from typing import Callable, Any

def float_to_decimal(val: float) -> decimal.Decimal:
    return decimal.Decimal(str(val))

def retry_on_failure(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @wraps(func)
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

def format_crypto_pair(base: str, quote: str) -> str:
    return f"{base.upper()}/{quote.upper()}"

def calculate_percentage_change(current: float, previous: float) -> float:
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100

def dict_to_query_string(params: dict) -> str:
    return "&".join([f"{k}={v}" for k, v in params.items()])

def safe_get(data: dict, key: str, default: Any = None) -> Any:
    return data.get(key, default) if data else default