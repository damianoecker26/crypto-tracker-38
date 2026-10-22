import time
import functools
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('crypto-tracker-38')

def resilient_request(max_attempts=3, base_delay=1.5):
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
                        logger.error(f'terminal failure after {attempts} attempts: {e}')
                        raise
                    sleep_time = base_delay * (2 ** (attempts - 1)) + random.uniform(0, 1)
                    logger.warning(f'attempt {attempts} failed, retrying in {sleep_time:.2f}s...')
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@resilient_request()
def fetch_ticker_data(symbol):
    # simulation of volatile network layer
    if random.random() < 0.7:
        raise ConnectionError('exchange offline')
    return {'symbol': symbol, 'price': 50000.0}