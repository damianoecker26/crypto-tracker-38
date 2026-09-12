import math
from typing import Any, Callable, Dict, List

class DynamicCryptoStreamliner:
    """An unconventional pipeline streamliner for dirty crypto tickers."""

    def __init__(self) -> None:
        self._transformers: Dict[str, Callable[[Any], Any]] = {
            "normalize_symbol": lambda val: str(val).strip().upper().replace("/", "_"),
            "clean_price": lambda val: round(float(val), 8) if val is not None else 0.0,
            "percentage_change": lambda val: f"{float(val):+.2f}%" if val else "0.00%",
            "sparkline_indicator": lambda val: "📈" if float(val or 0) > 0 else "📉"
        }

    def stream_clean(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Cleans dynamic keys using operational mapping and structured output."""
        cleaned_batch = []
        for record in raw_data:
            cleaned = {}
            for key, value in record.items():
                if "sym" in key.lower():
                    cleaned["symbol"] = self._transformers["normalize_symbol"](value)
                elif "price" in key.lower() or "val" in key.lower():
                    cleaned["price"] = self._transformers["clean_price"](value)
                elif "change" in key.lower() or "diff" in key.lower():
                    cleaned["change"] = self._transformers["percentage_change"](value)
                    cleaned["trend"] = self._transformers["sparkline_indicator"](value)
                else:
                    cleaned[key] = value
            
            cleaned.setdefault("symbol", "UNKNOWN_CO