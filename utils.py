import time
import functools
import random
import logging

logger = logging.getLogger('crypto-tracker-38')

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        logger.error(f'Failed after {retries} attempts: {e}')
                        raise
                    sleep_time = (backoff_in_seconds * 2 ** x + 
                                  random.uniform(0, 1))
                    logger.warning(f'Attempt {x+1} failed, retrying in {sleep_time:.2f}s...')
                    time.sleep(sleep_time)
                    x += 1
        return wrapper
    return decorator

@retry_with_backoff(retries=5, backoff_in_seconds=2)
def fetch_price_data(symbol):
    # Simulate network instability for crypto exchange API calls
    if random.random() < 0.7:
        raise ConnectionError('Exchange server overloaded')
    return {'symbol': symbol, 'price': random.uniform(10000, 60000)}