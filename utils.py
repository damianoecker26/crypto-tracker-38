import asyncio
import random
import time
from typing import Callable, Any

def fibonacci_sequence():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

def retry_on_crypto_failure(max_retries: int = 5, base_delay: float = 0.5):
    """
    Unusual retry decorator using a generator to calculate Fibonacci backoff
    with full jitter, designed for sensitive crypto API rate limits.
    """
    def decorator(func: Callable[..., Any]):
        async def async_wrapper(*args, **kwargs):
            fib = fibonacci_sequence()
            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise e
                    fib_num = next(fib)
                    delay = random.uniform(0, fib_num * base_delay)
                    print(f"[Attempt {attempt}/{max_retries}] Operation failed: {e}. Retrying in {delay:.2f}s...")
                    await asyncio.sleep(delay)

        def sync_wrapper(*args, **kwargs):
            fib = fibonacci_sequence()
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise e
                    fib_num = next(fib)
                    delay = random.uniform(0, fib_num * base_delay)
                    print(f"[Attempt {attempt}/{max_retries}] Operation failed: {e}. Retrying in {delay:.2f}s...")
                    time.sleep(delay)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator