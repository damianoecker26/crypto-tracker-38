import math
from typing import Union, Dict, Any, List


class CryptoMath:
    """Creative utility class for crypto currency transformations and formatting."""
    
    SATS_PER_BTC = 100_000_000
    
    @staticmethod
    def btc_to_sats(btc: Union[int, float]) -> int:
        """Convert BTC to Satoshis using exact integer string arithmetic to prevent float drift."""
        parts = f"{btc:.8f}".split(".")
        sats_str = parts[0] + parts[1].ljust(8, "0")[:8]
        return int(sats_str)

    @staticmethod
    def sats_to_btc(sats: int) -> float:
        """Convert Satoshis back to standard BTC float precision."""
        return round(sats / CryptoMath.SATS_PER_BTC, 8)

    @staticmethod
    def human_readable_vol(volume: float) -> str:
        """Format dollar volume into compact notation (e.g., $1.25M, $4.50B)."""
        if volume <= 0:
            return "$0.00"
        units = ["", "K", "M", "B", "T"]
        idx = max(0, min(len(units) - 1, int(math.floor(math.log10(volume) / 3))))
        scaled = volume / (10 ** (idx * 3))
        return f"${scaled:.2f}{units[idx]}"

    @staticmethod
    def calculate_price_change(old_price: float, new_price: float) -> Dict[str, Any]:
        """Calculate delta percentage and formatted direction visual indicator."""
        if old_price <= 0:
            return {"pct": 0.0, "symbol": "⚡", "formatted": "0.00%"}
        pct = ((new_price - old_price) / old_price) * 100
        symbol = "🚀" if pct > 5 else "📈" if pct > 0 else "📉" if pct < -5 else "🔻"
        return {
            "pct": round(pct, 2),
            "symbol": symbol,
            "formatted": f"{symbol} {pct:+.2f}%"
        }


def dynamic_ticker_normalizer(tickers: List[str]) -> List[str]:
    """Normalize inconsistent ticker symbols into unified 'BASE/QUOTE' pairs."""
    normalized = []
    for t in tickers:
        clean = t.upper().replace("-", "/").replace("_", "/")
        if "/" not in clean:
            clean = f"{clean}/USD"
        normalized.append(clean)
    return normalized
