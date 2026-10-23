import time
import functools
import logging

logger = logging.getLogger(__name__)

def retry_crypto_call(max_attempts=3, backoff_factor=1.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            delay = 1.0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f'Critical failure after {max_attempts} attempts')
                        raise e
                    
                    sleep_time = delay * (backoff_factor ** (attempts - 1))
                    logger.warning(f'Network wobble: {e}. Retrying in {sleep_time:.2f}s...')
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

@retry_crypto_call(max_attempts=4)
def fetch_price_data(ticker):
    # Simulate volatile network interactions for crypto endpoints
    import random
    if random.random() < 0.7:
        raise ConnectionError('Exchange API unresponsive')
    return {'ticker': ticker, 'price': 'moon-bound'}