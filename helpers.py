from typing import Any, Generator, Dict, Union, Iterable
import json
import math

def crypto_stream_normalizer(
    raw_stream: Iterable[Any], 
    smoothing_factor: float = 0.2
) -> Generator[Dict[str, float], None, None]:
    """
    Transforms raw heterogeneous crypto ticker data into a unified stream 
    with real-time Exponential Moving Average (EMA) calculated on-the-fly.
    """
    ema: Union[float, None] = None

    for item in raw_stream:
        match item:
            case {"symbol": sym, "price": p} if isinstance(p, (int, float, str)):
                symbol, price = str(sym).upper(), float(p)
            case (str(sym), int() | float() as p):
                symbol, price = sym.upper(), float(p)
            case str() as json_str:
                try:
                    parsed = json.loads(json_str)
                    symbol = str(parsed.get("symbol", "UNKNOWN")).upper()
                    price = float(parsed["price"])
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue
            case _:
                continue

        if math.isnan(price) or price <= 0:
            continue

        ema = price if ema is None else (price * smoothing_factor) + (ema * (1 - smoothing_factor))
        volatility_delta = abs(price - ema) / ema if ema else 0.0

        yield {
            "ticker": symbol,
            "raw_price": round(price, 8),
            "smoothed_ema": round(ema, 8),
            "volatility_index": round(volatility_delta, 6)
        }

def batch_aggregate_tickers(data_points: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    """Aggregates normalized crypto points into symbol-level metrics."""
    stats: Dict[str, Dict[str, float]] = {}
    for pt in data_points:
        sym = str(pt["ticker"])
        price = float(pt["raw_price"])
        ema = float(pt["smoothed_ema"])
        if sym not in stats:
            stats[sym] = {"min": price, "max": price, "last_ema": ema}
        else:
            stats[sym]["min"] = min(stats[sym]["min"], price)
            stats[sym]["max"] = max(stats[sym]["max"], price)
            stats[sym]["last_ema"] = ema
    return stats