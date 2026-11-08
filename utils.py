import time
import random
import functools
from typing import Callable, Any, Type, Tuple


def hodl_retry(
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    backoff_factor: float = 1.618,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """Golden-ratio jittered retry decorator for crypto network requests."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = base_delay
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    if attempt == max_retries:
                        raise err
                    jitter = random.uniform(0.8, 1.2)
                    sleep_time = min(delay * jitter, max_delay)
                    time.sleep(sleep_time)
                    delay *= backoff_factor
            return None
        return wrapper
    return decorator


def resilient_fetch(fetch_fn: Callable, *args: Any, **kwargs: Any) -> Any:
    """Functional wrapper executing network operations with proof-of-wait retries."""
    retrier = hodl_retry(max_retries=3, base_delay=0.5)(fetch_fn)
    return retrier(*args, **kwargs)
