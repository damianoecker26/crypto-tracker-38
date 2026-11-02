import time
import random
import functools
from typing import Callable, Any

def resilient_network_op(retries: int = 3, backoff: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= retries:
                        raise e
                    sleep_time = backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

class CryptoDataProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key

    @resilient_network_op(retries=5, backoff=1.0)
    def fetch_market_data(self, pair: str) -> dict:
        # Simulate network instability for crypto exchange API
        if random.random() < 0.3:
            raise ConnectionError(f"Failed to connect to exchange for {pair}")
        return {"pair": pair, "price": random.uniform(20000, 60000), "status": "success"}

if __name__ == "__main__":
    processor = CryptoDataProcessor(api_key="secret_key_99")
    data = processor.fetch_market_data("BTC/USD")
    print(f"Processed: {data}")