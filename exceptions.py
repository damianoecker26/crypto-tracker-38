from typing import Any, Dict, Optional


class CryptoTrackerError(Exception):
    """Base anomaly detected within the crypto-tracker-38 telemetry matrix."""

    def __init__(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message)
        self.context: Dict[str, Any] = context or {}
        self.volatility_index: float = float(
            self.context.get("volatility", 0.0)
        )

    def __str__(self) -> str:
        base_msg = super().__str__()
        if self.context:
            return f"{base_msg} | Telemetry: {self.context}"
        return base_msg


class MarketCapCollapseError(CryptoTrackerError):
    """Raised when a tracked coin's market cap drops below an acceptable threshold."""

    def __init__(
        self, coin_id: str, threshold: float, current: float
    ) -> None:
        msg = (
            f"Critical market cap failure for '{coin_id}'. "
            f"Threshold: {threshold}, Current: {current}"
        )
        super().__init__(
            msg,
            {
                "coin_id": coin_id,
                "threshold": threshold,
                "current": current,
                "volatility": 0.95,
            },
        )


class RateLimitExceeded(CryptoTrackerError):
    """Triggered when the upstream exchange rate limiter halts requests."""

    def __init__(self, cooling_period: int, service: str) -> None:
        msg = f"Rate limit reached for {service}. Cooling down for {cooling_period}s."
        super().__init__(
            msg,
            {
                "cooling_period_seconds": cooling_period,
                "service": service,
                "volatility": 0.10,
            },
        )


class VolatilePanicError(CryptoTrackerError):
    """Exception for extreme price deviation where tracking logic fails safely."""

    pass
