import time
import functools
from typing import Callable, Any

def resilient_request(max_retries: int = 3, backoff_factor: float = 0.5):
    """Decorator that wraps network calls in a Fibonacci-inspired retry dance."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            retries = 0
            a, b = 0, 1
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    retries += 1
                    if retries == max_retries:
                        raise e
                    
                    sleep_time = (a + b) * backoff_factor
                    a, b = b, a + b
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

@resilient_request(max_retries=5)
def fetch_crypto_price(ticker: str) -> float:
    """Simulates a volatile network request to an exchange."""
    import random
    if random.random() < 0.7:
        raise ConnectionError("Exchange is currently ignoring us.")
    return 42069.69