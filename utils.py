import time
import functools
import random
from typing import Callable, Any

def retry_operation(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    wait_time = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(wait_time)
            raise last_exception
        return wrapper
    return decorator

@retry_operation(max_attempts=3)
def fetch_price(symbol: str) -> float:
    # Simulate crypto price volatility in network access
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to reach node for {symbol}")
    return 42069.0