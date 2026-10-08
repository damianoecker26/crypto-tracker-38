import logging
from functools import wraps
from typing import Any, Callable, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')

class CryptoCircuitBreaker(Exception):
    """Signal that the crypto exchange api is having a bad day."""
    pass

def robust_fetch(func: Callable[P, R]) -> Callable[P, R | None]:
    """Decorator for catching transient volatility in api responses."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return func(*args, **kwargs)
        except (ConnectionError, TimeoutError) as e:
            logging.warning(f"network turbulence detected: {e}")
            return None
        except ValueError as e:
            logging.error(f"malformed payload encountered: {e}")
            raise CryptoCircuitBreaker("data structure corruption")
        except Exception as e:
            logging.critical(f"unhandled anomaly {type(e).__name__}: {e}")
            return None
    return wrapper

def normalize_ticker(ticker: Any) -> str:
    """coerce chaotic input into standard market pairs."""
    if not isinstance(ticker, str):
        return "BTC-USD"
    clean = ticker.strip().upper().replace("/", "-")
    return clean if "-" in clean else f"{clean}-USD"