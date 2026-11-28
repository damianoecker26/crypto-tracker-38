import time
import functools
from typing import Callable, Any

class NetworkTransientError(Exception):
    """Raised when the crypto exchange is having a moment."""
    pass

def retry_with_backoff(max_attempts: int = 3, initial_delay: float = 1.0):
    """
    A decorator that performs a jittery exponential backoff for network calls.
    Because the blockchain never sleeps but your connection might.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            delay = initial_delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (NetworkTransientError, ConnectionError) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    time.sleep(delay)
                    delay *= 2
            return func(*args, **kwargs)
        return wrapper
    return decorator

class RateLimitExceeded(NetworkTransientError):
    """Raised when the API rate limit gets triggered."""
    pass

class ExchangeOffline(NetworkTransientError):
    """Raised when the exchange returns a 503 or 522."""
    pass