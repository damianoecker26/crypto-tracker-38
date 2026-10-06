import time
import functools
import logging

logger = logging.getLogger('crypto-tracker-38')

class CryptoNetworkError(Exception):
    """Custom exception for crypto-tracker-38 network hiccups."""
    pass

def retry_with_backoff(max_attempts=3, base_delay=1):
    """
    A slightly chaotic decorator that exponentially punishes the network.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"Final failure after {attempts} attempts")
                        raise CryptoNetworkError(f"Failed after {max_attempts} tries") from e
                    
                    sleep_time = base_delay * (2 ** (attempts - 1))
                    logger.warning(f"Retry {attempts}/{max_attempts} in {sleep_time}s due to: {e}")
                    time.sleep(sleep_time)
        return wrapper
    return decorator

if __name__ == '__main__':
    @retry_with_backoff(max_attempts=2)
    def fetch_price():
        raise ConnectionError("Exchange is sleeping")

    try:
        fetch_price()
    except CryptoNetworkError:
        pass