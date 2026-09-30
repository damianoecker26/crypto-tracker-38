import time
import random
import functools
from typing import Callable, Any

def backoff_retry(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    if attempt < max_attempts - 1:
                        sleep_time = (base_delay * (2 ** attempt)) + (random.random() * 0.5)
                        time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

@backoff_retry(max_attempts=3, base_delay=0.5)
def fetch_crypto_price(ticker: str):
    # Simulate network instability in volatile crypto markets
    if random.random() < 0.7:
        raise ConnectionError(f"Exchange offline for {ticker}")
    return {"symbol": ticker, "price": random.uniform(1000, 60000)}