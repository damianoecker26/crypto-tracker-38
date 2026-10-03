import time
import random
from functools import wraps

def resilient_network_op(max_attempts=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    jitter = random.uniform(0, 0.5 * base_delay)
                    wait_time = (base_delay * (2 ** (attempts - 1))) + jitter
                    time.sleep(wait_time)
        return wrapper
    return decorator

class CryptoFetcher:
    @resilient_network_op(max_attempts=4, base_delay=2)
    def fetch_price(self, pair):
        import requests
        response = requests.get(f"https://api.exchange.com/v1/price/{pair}", timeout=5)
        response.raise_for_status()
        return response.json().get("price")