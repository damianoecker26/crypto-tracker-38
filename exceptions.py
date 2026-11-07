class CryptoTrackerError(Exception):
    """Base exception for all crypto-tracker-38 operations."""
    pass

class ExchangeConnectivityError(CryptoTrackerError):
    """Raised when the external exchange API times out."""
    pass

class PriceAnomalyDetected(CryptoTrackerError):
    """Raised when asset price fluctuates beyond logical bounds."""
    pass

class InvalidPayloadSchema(CryptoTrackerError):
    """Raised when incoming websocket data is malformed."""
    pass

def handle_crypto_exception(func):
    """Decorator for wrapping crypto operations in custom exception handlers."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError as e:
            raise ExchangeConnectivityError(f"Node connection failed: {e}") from e
        except KeyError as e:
            raise InvalidPayloadSchema(f"Missing expected schema field: {e}") from e
        except ValueError as e:
            raise PriceAnomalyDetected(f"Erroneous market data: {e}") from e
    return wrapper

class ExceptionReporter:
    """Unusual singleton-like utility for logging niche domain errors."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExceptionReporter, cls).__new__(cls)
        return cls._instance

    def log(self, exc: CryptoTrackerError):
        print(f"[CRITICAL-38] {exc.__class__.__name__}: {str(exc)}")