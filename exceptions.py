from typing import Optional, Any

class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-38 ecosystem."""
    def __init__(self, message: str, payload: Optional[Any] = None) -> None:
        super().__init__(message)
        self.payload: Optional[Any] = payload

class APIConnectionError(CryptoTrackerError):
    """Raised when the crypto exchange fails to respond."""
    def __init__(self, message: str = "Exchange heartbeat lost") -> None:
        super().__init__(message)

class RateLimitExceeded(CryptoTrackerError):
    """Raised when hitting gateway frequency constraints."""
    def __init__(self, retry_after: int = 60) -> None:
        super().__init__(f"Cooldown active for {retry_after} seconds", retry_after)

class DataValidationError(CryptoTrackerError):
    """Raised when market data fails sanity checks."""
    def __init__(self, field: str, value: Any) -> None:
        super().__init__(f"Invalid field {field} received: {value}", {"field": field, "value": value})

class SignatureVerificationError(CryptoTrackerError):
    """Raised when HMAC signatures fail validation."""
    def __init__(self, key_id: str) -> None:
        super().__init__(f"Invalid payload signature for key {key_id}")