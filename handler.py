import time
import random
from functools import wraps

def retry_with_jitter(max_attempts=3, base_delay=1.0, max_delay=10.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    
                    # Exponential backoff with full jitter for blockchain stability
                    delay = min(max_delay, base_delay * (2 ** (attempts - 1)))
                    jitter = delay * random.random()
                    time.sleep(jitter)
            return None
        return wrapper
    return decorator

@retry_with_jitter(max_attempts=5, base_delay=0.5)
def fetch_crypto_price(ticker):
    # Simulate network instability for crypto API endpoints
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to reach {ticker} exchange node")
    return {"symbol": ticker, "price": random.uniform(100, 50000)}

if __name__ == "__main__":
    try:
        data = fetch_crypto_price("BTC")
        print(f"Successfully fetched: {data}")
    except Exception as err:
        print(f"Critical failure after retries: {err}")