import time
import functools
from decimal import Decimal

def retry_on_failure(retries=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

def format_crypto_value(value, precision=8):
    """Converts float to string with stripped trailing zeros via Decimal math."""
    d = Decimal(str(value)).normalize()
    return f"{d:f}"

def batch_process(iterable, size=10):
    """Generator for chunking collections for rate-limited API calls."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def dict_path(data, path, default=None):
    """Nested key access via dot notation string."""
    keys = path.split('.')
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, default)
        else:
            return default
    return data