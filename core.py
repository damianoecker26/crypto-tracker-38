import json
from typing import Dict, Any, Generator, List, Union


class PayloadValidationError(ValueError):
    """Custom exception for payload validation failures."""
    pass


def validate_ticker_input(raw_input: Union[str, bytes]) -> Dict[str, Any]:
    """Validates incoming crypto ticker payload against strict rules."""
    if not isinstance(raw_input, (str, bytes)):
        raise PayloadValidationError("Input must be a JSON string or bytes")

    try:
        payload = json.loads(raw_input)
    except json.JSONDecodeError as err:
        raise PayloadValidationError(f"Invalid JSON syntax: {err}") from err

    if not isinstance(payload, dict):
        raise PayloadValidationError("Payload structure must be a JSON object")

    rules = {
        "symbol": lambda v: isinstance(v, str) and 2 <= len(v) <= 10 and v.isalnum(),
        "price": lambda v: isinstance(v, (int, float)) and v > 0,
        "volume_24h": lambda v: isinstance(v, (int, float)) and v >= 0,
        "timestamp": lambda v: isinstance(v, (int, float)) and v > 1000000000,
    }

    missing_fields = set(rules.keys()) - set(payload.keys())
    if missing_fields:
        raise PayloadValidationError(f"Missing required fields: {sorted(missing_fields)}")

    for field, validator in rules.items():
        if not validator(payload[field]):
            raise PayloadValidationError(f"Field validation failed for '{field}'")

    return {
        "symbol": payload["symbol"].upper(),
        "price": float(payload["price"]),
        "volume_24h": float(payload["volume_24h"]),
        "timestamp": int(payload["timestamp"]),
    }


def process_crypto_stream(data_stream: Generator[str, None, None]) -> List[Dict[str, Any]]:
    """Main processing loop consuming stream with inline input validation."""
    valid_ticks = []
    for raw_payload in data_stream:
        try:
            clean_data = validate_ticker_input(raw_payload)
            clean_data["liquidity_score"] = round(clean_data["price"] * clean_data["volume_24h"] / 1e6, 4)
            valid_ticks.append(clean_data)
        except PayloadValidationError:
            continue
    return valid_ticks