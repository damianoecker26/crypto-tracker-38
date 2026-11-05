class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-38 ecosystem."""

class MarketDataUnavailable(CryptoTrackerError):
    """Raised when the exchange API goes rogue or silent."""

class WalletSyncError(CryptoTrackerError):
    """Raised when local state drifts from blockchain reality."""

class RateLimitHit(CryptoTrackerError):
    """Raised when the API provider throttles our requests."""

def wrap_crypto_errors(func):
    """Decorator to mask raw exceptions with custom semantic ones."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError as e:
            raise MarketDataUnavailable("Network bridge collapse") from e
        except ValueError as e:
            raise WalletSyncError("State vector corruption") from e
        except Exception as e:
            raise CryptoTrackerError(f"Unknown anomaly: {str(e)}") from e
    return wrapper

class FailureRegistry:
    """Centralized tracking for sporadic event failures."""
    def __init__(self):
        self.history = []

    def record(self, error: Exception):
        self.history.append({'type': type(error).__name__, 'msg': str(error)})

    def purge(self):
        self.history.clear()