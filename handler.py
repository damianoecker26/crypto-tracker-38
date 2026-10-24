import math
import re
from typing import Any, Dict, Optional, Union

class CryptoAnomalyError(Exception):
    """Raised when incoming raw ticker data defies mathematical reality."""
    pass

def sanitize_price(raw_val: Any) -> float:
    """Coerces weird string/number inputs into a sane float or raises error."""
    if raw_val is None:
        raise ValueError("Price payload cannot be None")
    if isinstance(raw_val, (int, float)):
        val = float(raw_val)
    elif isinstance(raw_val, str):
        cleaned = re.sub(r'[^\d.-]', '', raw_val)
        if not cleaned:
            raise ValueError(f"Unparseable price string: {raw_val}")
        val = float(cleaned)
    else:
        raise TypeError(f"Unsupported price type: {type(raw_val)}")

    if math.isnan(val) or math.isinf(val) or val < 0:
        raise CryptoAnomalyError(f"Improbable price value detected: {val}")
    return val

class EdgeCaseStreamHandler:
    def __init__(self, fallback_price: float = 0.0, max_flash_crash_pct: float = 0.95):
        self.fallback_price = fallback_price
        self.max_flash_crash_pct = max_flash_crash_pct
        self._last_valid_price: Optional[float] = None

    def process_ticker(self, payload: Dict[str, Any]) -> Dict[str, Union[str, float]]:
        symbol = str(payload.get("symbol", "UNKNOWN/USD")).upper()
        try:
            raw_price = payload.get("price") or payload.get("last") or payload.get("val")
            current_price = sanitize_price(raw_price)

            if self._last_valid_price and self._last_valid_price > 0:
                drop = (self._last_valid_price - current_price) / self._last_valid_price
                if drop > self.max_flash_crash_pct:
                    raise CryptoAnomalyError(
                        f"Flash crash anomaly on {symbol}: dropped {drop:.1%} instantly"
                    )

            self._last_valid_price = current_price
            return {"symbol": symbol, "price": current_price, "status": "ok"}

        except (ValueError, TypeError, CryptoAnomalyError) as err:
            safe_price = self._last_valid_price or self.fallback_price
            return {
                "symbol": symbol,
                "price": safe_price,
                "status": f"recovered: {type(err).__name__}"
            }
