import functools
import logging
import time

logger = logging.getLogger('crypto-tracker-38')

class CryptoError(Exception):
    """Base exception for anomalous market conditions."""
    pass

def resilient_fetch(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logger.warning(f"Attempt {attempt+1} failed for {func.__name__}")
                    time.sleep(delay * (2 ** attempt))
                except Exception as e:
                    logger.error(f"Unrecoverable anomaly: {e}")
                    raise CryptoError(f"Market disruption in {func.__name__}: {e}") from e
            raise last_ex
        return wrapper
    return decorator

def sanitize_price(value):
    try:
        clean = float(value)
        if clean < 0:
            raise ValueError("Negative price detected")
        return clean
    except (TypeError, ValueError) as e:
        logger.debug(f"Sanitization failure: {value}, defaulting to 0.0")
        return 0.0

def validate_ticker(ticker):
    if not isinstance(ticker, str) or len(ticker) < 2:
        raise ValueError(f"Malformed asset ticker: {ticker}")
    return ticker.upper()