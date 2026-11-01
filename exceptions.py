"""Domain-specific exception hierarchy for crypto-tracker-38 with rich contextual diagnostics."""

from typing import Any, Dict, Optional, Union
import time


class CryptoTrackerError(Exception):
    """Base exception class for all crypto tracking operational failures.

    Supports dynamic context payloads for telemetry and automated diagnostic logging.
    """

    def __init__(
        self,
        message: str,
        symbol: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message: str = message
        self.symbol: Optional[str] = symbol.upper() if symbol else None
        self.metadata: Dict[str, Any] = metadata or {}
        self.timestamp: float = time.time()

    def telemetry_payload(self) -> Dict[str, Union[str, float, Dict[str, Any]]]:
        """Generates a structured dictionary representation of the error event."""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "symbol": self.symbol or "GLOBAL",
            "timestamp": self.timestamp,
            "context": self.metadata,
        }

    def __str__(self) -> str:
        symbol_prefix: str = f"[{self.symbol}] " if self.symbol else ""
        return f"{symbol_prefix}{self.message}"


class RateLimitExceededError(CryptoTrackerError):
    """Raised when an API endpoint enforces request throttling."""

    def __init__(
        self,
        provider: str,
        retry_after: float = 60.0,
        symbol: Optional[str] = None,
    ) -> None:
        self.provider: str = provider
        self.retry_after: float = max(0.0, float(retry_after))
        msg: str = f"Rate limit breached on {provider}. Backoff required: {self.retry_after:.1f}s"
        super().__init__(msg, symbol=symbol, metadata={"provider": provider, "retry_after": self.retry_after})

    def is_cooling_down(self) -> bool:
        """Determines if the mandatory retry window is still active."""
        return (time.time() - self.timestamp) < self.retry_after


class SlippageToleranceExceededError(CryptoTrackerError):
    """Raised when expected order execution price deviates beyond threshold limits."""

    def __init__(
        self,
        expected_price: float,
        actual_price: float,
        tolerance_pct: float,
        symbol: str,
    ) -> None:
        self.expected_price: float = expected_price
        self.actual_price: float = actual_price
        self.tolerance_pct: float = tolerance_pct
        self.deviation_pct: float = abs((actual_price - expected_price) / expected_price) * 100.0
        
        msg: str = f"Slippage violation: observed {self.deviation_pct:.2f}% (max allowed: {tolerance_pct:.2f}%)"
        super().__init__(
            msg,
            symbol=symbol,
            metadata={
                "expected": expected_price,
                "actual": actual_price,
                "allowed_tolerance": tolerance_pct,
                "realized_deviation": self.deviation_pct,
            },
        )
