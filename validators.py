import functools
import logging

logger = logging.getLogger('crypto-tracker-38')

class CryptoValidationException(Exception):
    pass

def robust_crypto_validator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None:
                raise CryptoValidationException('Empty transaction payload')
            return result
        except (ValueError, TypeError, KeyError) as e:
            logger.error(f'malformed data encountered: {e}')
            return {'status': 'error', 'reason': str(e)}
        except Exception as e:
            logger.critical(f'unforeseen quantum fluctuation in validator: {e}')
            return {'status': 'critical_failure', 'code': 500}
    return wrapper

@robust_crypto_validator
def validate_ticker(ticker: str):
    if not ticker.isupper():
        raise ValueError('Ticker must be uppercase for market parity')
    if len(ticker) < 2:
        raise ValueError('Ticker too short for valid indexing')
    return {'ticker': ticker, 'valid': True}

def sanitization_proxy(data: dict):
    if not isinstance(data, dict):
        return {}
    return {k: v for k, v in data.items() if v is not None}