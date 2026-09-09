import time
import functools
import random
from typing import Callable, Any

def retry_with_exponential_backoff(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                        time.sleep(sleep_time)
            raise last_exception
        return wrapper
    return decorator

def network_operation_wrapper(func: Callable):
    return retry_with_exponential_backoff(max_attempts=5, base_delay=0.5)(func)

# Example usage for crypto-tracker-38
@network_operation_wrapper
def fetch_crypto_price(ticker: str):
    # Simulate network instability
    if random.random() < 0.7:
        raise ConnectionError(f'Market chaos: {ticker} unreachable')
    return f'{ticker}: $42069.00'