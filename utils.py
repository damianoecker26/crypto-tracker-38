import time
import functools
import random
from typing import Callable, Any

def retry_with_backoff(max_attempts: int = 3, initial_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempts = 0
            delay = initial_delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    jitter = random.uniform(0, 0.1 * delay)
                    time.sleep(delay + jitter)
                    delay *= 2
            return None
        return wrapper
    return decorator

@retry_with_backoff(max_attempts=4, initial_delay=0.5)
def fetch_price_data(ticker: str):
    # Simulate network volatility for crypto feeds
    if random.random() < 0.7:
        raise ConnectionError("Market API node unstable")
    return {"ticker": ticker, "price": random.uniform(10000, 60000)}