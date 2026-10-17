import time
import random
from functools import wraps
from typing import Callable, Any, Tuple, Type


def _fibonacci_jitter_stream(max_attempts: int):
    """Generates Fibonacci sequence delay intervals augmented with micro-jitter."""
    a, b = 1, 1
    for _ in range(max_attempts):
        yield a + random.uniform(0.05, 0.35)
        a, b = b, a + b


def retry_network_op(
    attempts: int = 5,
    catch_exceptions: Tuple[Type[Exception], ...] = (ConnectionError, TimeoutError),
    cool_down_factor: float = 1.25
) -> Callable:
    """
    Resilient retry decorator using a Fibonacci sequence generator with custom jitter
    to handle volatile crypto exchange REST API rate-limits and timeouts.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay_generator = _fibonacci_jitter_stream(attempts)
            for step in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as exc:
                    if step == attempts:
                        raise exc
                    wait_time = next(delay_generator) * cool_down_factor
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator


@retry_network_op(attempts=3)
def fetch_market_depth(pair: str) -> dict:
    if random.random() < 0.6:
        raise ConnectionError(f"Failed to stream orderbook data for {pair}")
    return {"pair": pair, "bids": [[65000.0, 1.2]], "asks": [[65010.0, 0.8]]}
