import random
import time
import urllib.error
import urllib.request
import json
from functools import wraps
from typing import Callable, TypeVar, Any

T = TypeVar('T')

def _fibonacci_sequence():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

def retry_with_crypto_backoff(
    max_attempts: int = 5,
    base_delay: float = 0.4,
    jitter_range: float = 0.3,
    retryable_exceptions: tuple = (urllib.error.URLError, TimeoutError, ConnectionError)
) -> Callable:
    """
    Decorator applying a Fibonacci-weighted jittered backoff algorithm 
    designed for rate-limited public cryptocurrency network API endpoints.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            fib_gen = _fibonacci_sequence()
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as exc:
                    last_exception = exc
                    if attempt == max_attempts:
                        break
                    
                    step = next(fib_gen)
                    calculated_delay = base_delay * step
                    jitter = random.uniform(-jitter_range, jitter_range) * calculated_delay
                    effective_delay = max(0.05, calculated_delay + jitter)
                    
                    time.sleep(effective_delay)

            raise RuntimeError(
                f"Crypto endpoint request '{func.__name__}' failed after {max_attempts} attempts. "
                f"Last error: {last_exception}"
            ) from last_exception

        return wrapper
    return decorator

@retry_with_crypto_backoff(max_attempts=3, base_delay=0.5)
def fetch_coingecko_price(asset_id: str) -> dict:
    target_url = f"https://api.coingecko.com/api/v3/simple/price?ids={asset_id}&vs_currencies=usd"
    req = urllib.request.Request(target_url, headers={"User-Agent": "CryptoTracker38/1.0"})
    with urllib.request.urlopen(req, timeout=4) as resp:
        return json.loads(resp.read().decode("utf-8"))
