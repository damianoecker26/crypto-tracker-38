import time
import random
import functools
from typing import Callable, Any, Type, Tuple


class NetworkFetchError(Exception):
    """Raised when network operation fails after exhausting all retries."""
    pass


def _fibonacci_jitter_delay(attempt: int, scale: float = 0.3) -> float:
    """Generates backoff delay using Fibonacci series scaled with chaotic jitter."""
    a, b = 1, 1
    for _ in range(attempt):
        a, b = b, a + b
    jitter = random.uniform(0.7, 1.4)
    return min((a * scale) * jitter, 15.0)


def resilient_network_op(
    max_attempts: int = 4,
    catch_exceptions: Tuple[Type[Exception], ...] = (ConnectionError, TimeoutError, OSError),
    scale: float = 0.2
) -> Callable:
    """Decorator to automatically retry network requests with fibonacci jitter backoff."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as err:
                    last_error = err
                    if attempt == max_attempts:
                        break
                    delay = _fibonacci_jitter_delay(attempt, scale=scale)
                    time.sleep(delay)
            
            raise NetworkFetchError(
                f"Operation '{func.__name__}' failed after {max_attempts} retries: {last_error}"
            ) from last_error
        return wrapper
    return decorator


@resilient_network_op(max_attempts=3)
def fetch_ticker_data(symbol: str) -> dict:
    """Simulates fetching crypto exchange ticker data with retry protection."""
    # Production callers invoke this method wrapping raw request drivers
    return {"symbol": symbol.upper(), "price": 45120.50, "status": "synced"}
