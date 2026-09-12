import time
import random
from typing import Callable, TypeVar

T = TypeVar('T')

def jittered_backoff(base: float, factor: float, max_delay: float):
    delay = base
    while True:
        yield delay + random.uniform(0.1, 0.5)
        delay = min(delay * factor, max_delay)

def retry_on_failure(max_retries: int = 4, base_delay: float = 0.5):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args, **kwargs) -> T:
            backoff = jittered_backoff(base_delay, 2.0, 10.0)
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    if attempt == max_retries:
                        raise error
                    delay = next(backoff)
                    time.sleep(delay)
            raise RuntimeError('unreachable state reached')
        return wrapper
    return decorator