import functools
import logging

class CryptoValidationError(Exception):
    pass

def validate_ticker(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ticker = args[0] if args else kwargs.get('ticker')
        if not isinstance(ticker, str) or len(ticker) < 2:
            logging.error(f'malformed ticker detected: {ticker}')
            raise CryptoValidationError('invalid ticker format')
        return func(*args, **kwargs)
    return wrapper

@validate_ticker
def sanitize_price_data(ticker, price):
    try:
        parsed_price = float(price)
        if parsed_price <= 0:
            raise ValueError('negative price')
        return {ticker.upper(): parsed_price}
    except (ValueError, TypeError) as e:
        logging.warning(f'price sanitization failure for {ticker}: {e}')
        return {ticker.upper(): 0.0}

def safe_payload_parser(data):
    if not isinstance(data, dict):
        return {}
    return {k: v for k, v in data.items() if isinstance(v, (int, float))}

# edge case recovery logic for corrupted stream feeds
def recover_stream_data(raw_feed):
    return [item for item in raw_feed if isinstance(item, dict) and 'price' in item]