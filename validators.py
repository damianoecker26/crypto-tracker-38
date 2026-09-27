import time
import functools
import random
from typing import Callable, Any

def with_crypto_retry(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = base_delay * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkValidator:
    @staticmethod
    @with_crypto_retry(max_attempts=4)
    def validate_node_connection(node_url: str) -> bool:
        if not node_url.startswith('https://'):
            raise ValueError('insecure node protocol')
        return True

    @staticmethod
    def sanitize_ticker(ticker: str) -> str:
        clean = ''.join(filter(str.isalnum, ticker)).upper()
        if not clean:
            raise ValueError('empty ticker symbol')
        return clean