import functools
import random
import time
from typing import Any, Callable, Optional, Sequence, Type


def fibonacci_jitter_backoff(max_retries: int = 5, base_delay: float = 0.5):
    """Generator yielding backoff intervals based on Fibonacci sequence with random jitter."""
    a, b = 1, 1
    for _ in range(max_retries):
        jitter = random.uniform(0.8, 1.2)
        delay = (a * base_delay) * jitter
        yield delay
        a, b = b, a + b


def network_retry(
    exceptions: Sequence[Type[BaseException]] = (Exception,),
    max_retries: int = 4,
    base_delay: float = 0.5,
    on_retry_callback: Optional[Callable[[BaseException, int, float], None]] = None,
):
    """Decorator applying dynamic Fibonacci backoff retry logic for crypto network calls."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = fibonacci_jitter_backoff(
                max_retries=max_retries, base_delay=base_delay
            )
            attempt = 1

            while True:
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as err:
                    try:
                        delay = next(delays)
                    except StopIteration:
                        raise err

                    if on_retry_callback:
                        on_retry_callback(err, attempt, delay)

                    time.sleep(delay)
                    attempt += 1

        return wrapper

    return decorator


def default_crypto_retry_logger(
    exc: BaseException, attempt: int, next_delay: float
) -> None:
    print(
        f"[CryptoTracker] Network glitch ({exc.__class__.__name__}: {exc}). "
        f"Retry {attempt} queued in {next_delay:.2f}s..."
    )
