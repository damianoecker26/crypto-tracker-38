import time
import functools
import random
from typing import Callable, Any

def retry_operation(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        jitter = random.uniform(0, 0.1 * base_delay)
                        sleep_time = (base_delay * (2 ** attempt)) + jitter
                        time.sleep(sleep_time)
                    continue
            raise last_exception
        return wrapper
    return decorator

@retry_operation(max_attempts=3)
def validate_crypto_payload(data: dict) -> bool:
    if 'price' not in data or 'symbol' not in data:
        raise ValueError('Incomplete crypto data packet')
    return True