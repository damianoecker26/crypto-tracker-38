import time
import functools
import random
from typing import Callable, Any

def backoff_retry(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

@backoff_retry(max_attempts=3)
def fetch_price(symbol: str) -> float:
    # Simulate crypto api calls
    if random.random() < 0.7:
        raise ConnectionError('Market data nodes unresponsive')
    return 50000.0 + random.uniform(-100, 100)