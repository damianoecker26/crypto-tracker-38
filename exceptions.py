class CryptoError(Exception):
    """Base exception for all crypto-tracker-38 modules."""

class MarketVolatiliyError(CryptoError):
    """Raised when price variance exceeds safety thresholds."""

class NetworkTimeoutError(CryptoError):
    """Wrapped exception for flaky exchange API connections."""

class DataSanityError(CryptoError):
    """Raised when payload looks like garbage or corrupted."""

def raise_if_unstable(price_diff: float, limit: float = 0.5):
    """Unusual checker that yells if market movement is sus."""
    if abs(price_diff) > limit:
        raise MarketVolatiliyError(f"Market movement of {price_diff} is too volatile.")

class CryptoExceptionHandler:
    """Context manager for suppressing noise in data streams."""
    def __init__(self, logger):
        self.logger = logger

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.error(f"Anomaly detected: {exc_val}")
            return isinstance(exc_val, CryptoError)
        return True