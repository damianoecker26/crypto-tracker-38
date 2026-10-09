import math
import decimal
from typing import Any, Dict, Union

class CryptoDataError(Exception):
    """Raised when a crypto metric calculation fails fatally."""
    pass

def safe_parse_amount(val: Any, default: float = 0.0) -> float:
    """Parses malformed, scientific notation, or stringified crypto amounts safely."""
    if val is None:
        return default
    try:
        cleaned = str(val).strip().replace(",", "")
        d = decimal.Decimal(cleaned)
        if d.is_nan() or d.is_infinite():
            return default
        return float(d)
    except (decimal.InvalidOperation, ValueError, TypeError):
        return default

def resilient_ratio(numerator: Any, denominator: Any, fallback: float = 0.0) -> float:
    """Calculates crypto ratio avoiding division-by-zero or floating overflow."""
    num = safe_parse_amount(numerator, default=0.0)
    den = safe_parse_amount(denominator, default=0.0)

    if math.isclose(den, 0.0, abs_tol=1e-12) or den <= 0:
        return fallback

    result = num / den
    return fallback if (math.isnan(result) or math.isinf(result)) else result

def sanitize_ticker_payload(payload: Dict[str, Any]) -> Dict[str, Union[float, str]]:
    """Sanitizes raw web API ticker payload with edge-case fallback standardizations."""
    if not isinstance(payload, dict):
        raise CryptoDataError(f"Expected dict payload, got {type(payload).__name__}")

    expected_keys = ("price", "volume", "market_cap", "change_24h")
    sanitized = {}

    for key in expected_keys:
        parsed = safe_parse_amount(payload.get(key), default=0.0)
        if key == "price" and parsed < 0:
            parsed = 0.0
        sanitized[key] = parsed

    sanitized["vol_mc_ratio"] = resilient_ratio(
        sanitized["volume"], sanitized["market_cap"]
    )
    sanitized["symbol"] = str(payload.get("symbol", "UNKNOWN")).upper().strip()
    return sanitized
