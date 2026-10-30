import time
import functools
import random
from typing import Callable, Any

def retry_with_backoff(max_attempts: int = 3, initial_delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = initial_delay * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

@retry_with_backoff(max_attempts=4)
def fetch_price_data(ticker: str) -> dict:
    # Simulation of unpredictable crypto network behavior
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to reach node for {ticker}")
    return {"ticker": ticker, "price": 42069.0}