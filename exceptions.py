import logging
import re
from typing import Any, Callable

logger = logging.getLogger("crypto_tracker.exceptions")


class CryptoTrackerError(Exception):
    """Base exception for all cryptocurrency tracker operations."""


class PriceAnomalyError(CryptoTrackerError):
    """Raised when a price value is physically impossible or anomalous."""


class RecoveryManager:
    """Unusual healing engine to salvage corrupted price strings from erratic APIs."""

    @staticmethod
    def salvage_price(corrupted_value: Any) -> float:
        if isinstance(corrupted_value, (int, float)):
            if corrupted_value <= 0:
                raise PriceAnomalyError(
                    f"Non-positive price encountered: {corrupted_value}"
                )
            return float(corrupted_value)

        raw_str = str(corrupted_value).strip()
        # Eliminate common weird noise like currency symbols, spaces, commas
        cleaned = re.sub(r"[^0-9.-]", "", raw_str)

        # Fix multi-decimal points (e.g., '12.34.56') by preserving only the first
        if cleaned.count(".") > 1:
            parts = cleaned.split(".")
            cleaned = f"{parts[0]}.{''.join(parts[1:])}"

        try:
            parsed = float(cleaned)
            if parsed <= 0:
                raise PriceAnomalyError(
                    f"Parsed price is non-positive: {parsed}"
                )
            return parsed
        except ValueError as err:
            raise PriceAnomalyError(
                f"Failed to salvage price from raw data '{corrupted_value}'"
            ) from err


def auto_recovery(
    fallback_value: float,
) -> Callable[[Callable[..., float]], Callable[..., float]]:
    """Decorator that attempts price salvage recovery before yielding to a fallback."""

    def decorator(func: Callable[..., float]) -> Callable[..., float]:
        def wrapper(*args: Any, **kwargs: Any) -> float:
            try