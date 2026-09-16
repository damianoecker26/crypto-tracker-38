import time
import functools
import random
import logging

logger = logging.getLogger('crypto-tracker-38')

class CryptoNetworkError(Exception):
    pass

def retry_on_failure(max_attempts=3, backoff=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        logger.error(f'Critical failure after {attempts} attempts')
                        raise CryptoNetworkError(f'Network failure: {str(e)}')
                    sleep_time = backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    logger.warning(f'Retrying {func.__name__} in {sleep_time:.2f}s...')
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class RateLimitExceeded(CryptoNetworkError):
    pass

class ExchangeTimeout(CryptoNetworkError):
    pass