import time
import functools
import logging

logger = logging.getLogger('crypto-tracker-38')

class NetworkRetry:
    def __init__(self, max_retries=3, delay=1.5, backoff=2):
        self.max_retries = max_retries
        self.delay = delay
        self.backoff = backoff

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tries, current_delay = 0, self.delay
            while tries < self.max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    tries += 1
                    if tries == self.max_retries:
                        logger.error(f'Critical network failure after {tries} attempts')
                        raise e
                    logger.warning(f'Retry {tries}/{self.max_retries} due to {e}')
                    time.sleep(current_delay)
                    current_delay *= self.backoff
        return wrapper

def resilient(func):
    return NetworkRetry()(func)

class CryptoNetworkError(Exception):
    """Custom base exception for network disruptions in crypto-tracker-38."""
    pass