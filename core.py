import json
import logging
from typing import Any, Generator, Dict

logger = logging.getLogger("crypto_tracker")


class PayloadValidationError(ValueError):
    """Raised when incoming streaming payload fails verification."""
    pass


def validate_raw_tick(data: Any) -> Dict[str, Any]:
    """Validates dynamic dynamic-typed tick payloads with strict schema constraints."""
    if isinstance(data, (bytes, str)):
        try:
            data = json.loads(data)
        except Exception as err:
            raise PayloadValidationError(f"Malformed JSON payload: {err}") from err

    if not isinstance(data, dict):
        raise PayloadValidationError(f"Payload must be object, got {type(data).__name__}")

    required = {"pair": str, "price": (int, float), "volume": (int, float)}
    sanitized = {}
    
    for key, expected_type in required.items():
        if key not in data:
            raise PayloadValidationError(f"Missing required field: '{key}'")
        val = data[key]
        if not isinstance(val, expected_type) or isinstance(val, bool):
            raise PayloadValidationError(f"Field '{key}' invalid type: expected {expected_type}")
        sanitized[key] = val

    if sanitized["price"] <= 0 or sanitized["volume"] < 0:
        raise PayloadValidationError(f"Out-of-range market metrics: {sanitized}")

    return sanitized


def run_market_loop(feed: Generator[Any, None, None]) -> Generator[Dict[str, Any], None, None]:
    """Main processing loop filtering bad updates via validation guards."""
    for raw_item in feed:
        try:
            clean_tick = validate_raw_tick(raw_item)
            yield clean_tick
        except PayloadValidationError as exc:
            logger.warning("Discarded corrupt ticker event: %s", exc)
            continue
