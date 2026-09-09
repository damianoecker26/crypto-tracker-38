import time
import functools
import logging

logger = logging.getLogger('crypto-tracker-38')

class CryptoError(Exception):
    pass

def resilient_fetch(max_retries=3, backoff=2):
    """Decorator applying jittered exponential backoff for crypto APIs."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    wait = backoff ** attempts
                    logger.warning(f"Attempt {attempts} failed: {e}. Retrying in {wait}s")
                    if attempts == max_retries:
                        raise CryptoError(f"API exhaustion after {max_retries} attempts") from e
                    time.sleep(wait)
            return None
        return wrapper
    return decorator

def sanitize_price(raw_val):
    """Enforce numeric integrity on volatile ticker strings."""
    try:
        clean = float(str(raw_val).replace(',', ''))
        if clean < 0:
            raise ValueError("Negative price detected")
        return clean
    except (ValueError, TypeError, AttributeError):
        logger.error(f"Malformed price data: {raw_val}")
        return 0.0

def validate_ticker(ticker):
    """Strict validation for crypto symbol naming conventions."""
    if not isinstance(ticker, str) or not (2 <= len(ticker) <= 10):
        raise CryptoError(f"Invalid ticker format: {ticker}")
    return ticker.upper()