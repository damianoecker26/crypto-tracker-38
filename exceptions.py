from typing import Optional, Any

class CryptoTrackerError(Exception):
    """Base exception for all crypto-tracker-38 failures."""
    def __init__(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.context: dict[str, Any] = context or {}

class APIConnectionError(CryptoTrackerError):
    """Raised when the exchange API decides to ghost us."""
    pass

class DataNormalizationError(CryptoTrackerError):
    """Raised when the payload is absolute nonsense."""
    pass

class RateLimitExceeded(CryptoTrackerError):
    """Raised when the rate limit hammer hits our requests."""
    def __init__(self, retry_after: int) -> None:
        super().__init__(f"Cooldown required for {retry_after} seconds", {"wait": retry_after})

class ConfigurationMismatch(CryptoTrackerError):
    """Raised when environment variables are living in fantasy land."""
    pass