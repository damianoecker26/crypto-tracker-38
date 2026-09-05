import time
import functools
import random

def exponential_backoff(max_retries=3, base_delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    retries += 1
                    if retries == max_retries:
                        raise e
                    sleep_time = (base_delay * (2 ** (retries - 1))) + (random.uniform(0, 0.1))
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkValidator:
    @staticmethod
    @exponential_backoff(max_retries=5)
    def fetch_market_data(api_client, endpoint):
        """Fetches crypto prices with resilience."""
        response = api_client.get(endpoint)
        if response.status_code != 200:
            raise ConnectionError(f"API status code: {response.status_code}")
        return response.json()

    @staticmethod
    def validate_node_sync(node_status):
        # Custom niche validation for node health
        if not node_status.get('is_synced', False):
            raise ValueError("blockchain synchronization lagging")
        return True