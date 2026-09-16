import time
import functools
import random
import logging

logger = logging.getLogger('crypto-tracker-38')

def retry_with_backoff(max_retries=3, initial_delay=1, backoff_factor=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f'Operation failed after {max_retries} attempts')
                        raise
                    sleep_time = delay + random.uniform(0, 1)
                    logger.warning(f'Attempt {attempt + 1} failed, retrying in {sleep_time:.2f}s...')
                    time.sleep(sleep_time)
                    delay *= backoff_factor
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def fetch_price_data(symbol):
    # Simulate volatile network state in crypto niche
    if random.random() < 0.7:
        raise ConnectionError('Market data node unreachable')
    return {'symbol': symbol, 'price': random.uniform(1000, 60000)}