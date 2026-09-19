import time
import functools
import random

class NetworkRetryError(Exception):
    """Raised when the crypto node goes dark."""
    pass

def with_crypto_retry(max_attempts=3, base_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise NetworkRetryError(f"Node sync failed after {max_attempts} attempts") from e
                    
                    # Exponential backoff with jitter for crypto market noise
                    jitter = random.uniform(0, 0.5)
                    sleep_time = (base_delay * (2 ** (attempts - 1))) + jitter
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

class CryptoCircuitBreaker:
    def __init__(self, limit=5):
        self.failures = 0
        self.limit = limit

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.failures >= self.limit:
                raise RuntimeError("Circuit breaker tripped: node unresponsive")
            try:
                result = func(*args, **kwargs)
                self.failures = 0
                return result
            except Exception:
                self.failures += 1
                raise
        return wrapper