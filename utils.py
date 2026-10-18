from typing import Dict, Any, List, Callable

class CryptoPipe:
    """Functional pipeline operator for real-time crypto stream processing."""
    def __init__(self, func: Callable):
        self.func = func

    def __rshift__(self, other: "CryptoPipe") -> "CryptoPipe":
        return CryptoPipe(lambda stream: other.func(self.func(stream)))

    def __call__(self, stream: Any) -> Any:
        return self.func(stream)

def parse_tickers(stream: List[Dict[str, Any]]) -> List[Dict[str, float]]:
    """Extracts and normalizes price and volume payload."""
    return [
        {
            "symbol": str(t["symbol"]).upper(),
            "price": float(t["price"]),
            "volume": float(t["volume"])
        }
        for t in stream
        if all(k in t for k in ("symbol", "price", "volume"))
    ]

def calculate_vwap(ticks: List[Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    """Calculates volume-weighted average price per crypto symbol."""
    acc: Dict[str, Dict[str, float]] = {}
    for t in ticks:
        sym = t["symbol"]
        if sym not in acc:
            acc[sym] = {"total_pv": 0.0, "total_vol": 0.0, "count": 0}
        acc[sym]["total_pv"] += t["price"] * t["volume"]
        acc[sym]["total_vol"] += t["volume"]
        acc[sym]["count"] += 1

    return {
        sym: {
            "vwap": round(stats["total_pv"] / stats["total_vol"], 4) if stats["total_vol"] else 0.0,
            "volume": round(stats["total_vol"], 2),
            "count": int(stats["count"])
        }
        for sym, stats in acc.items()
    }

def process_crypto_payload(raw_data: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    """Pipeline entry point chaining parse and calculation functions."""
    pipeline = CryptoPipe(parse_tickers) >> CryptoPipe(calculate_vwap)
    return pipeline(raw_data)
