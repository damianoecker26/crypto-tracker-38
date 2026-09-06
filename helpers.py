import time
import functools
from typing import Callable, Any

def time_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f'[DEBUG] {func.__name__} took {elapsed:.6f}s')
        return result
    return wrapper

def retry_on_failure(retries: int = 3, delay: float = 1.0):
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

def format_crypto_amount(val: float, precision: int = 8) -> str:
    return f"{val:.{precision}f}".rstrip('0').rstrip('.')

def dict_path(data: dict, path: str, default: Any = None) -> Any:
    keys = path.split('.')
    for key in keys:
        if isinstance(data, dict): data = data.get(key)
        else: return default
    return data if data is not None else default