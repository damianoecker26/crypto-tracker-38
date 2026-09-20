import time
import functools
import random
import logging

logger = logging.getLogger('crypto-tracker-38')

def exponential_backoff(max_retries=5, base_delay=1.0, jitter=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError, Exception) as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f'Critical failure after {max_retries} attempts: {e}')
                        raise
                    
                    delay = base_delay * (2 ** (retries - 1))
                    if jitter:
                        delay *= (0.5 + random.random())
                    
                    logger.warning(f'Network anomaly detected. Retry {retries}/{max_retries} in {delay:.2f}s...')
                    time.sleep(delay)
        return wrapper
    return decorator

@exponential_backoff(max_retries=3)
def fetch_price_data(ticker):
    # Simulate volatile crypto network behavior
    if random.random() < 0.7:
        raise ConnectionError('Exchange node unstable')
    return {'ticker': ticker, 'price': random.uniform(100, 50000)}