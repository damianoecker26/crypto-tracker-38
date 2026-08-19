import time
import requests

class NetworkError(Exception):
    pass


def retry_request(url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise NetworkError(f'Failed to fetch {url} after {retries} attempts') from e


def get_crypto_price(crypto):
    url = f'https://api.cryptocurrency.com/{crypto}/price'
    return retry_request(url)


def get_market_data():
    url = 'https://api.cryptocurrency.com/market'
    return retry_request(url)
