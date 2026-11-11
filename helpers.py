import math
from typing import Dict, List, Tuple, Generator, Union


class ComplexTicker:
    """Crypto stream helper utilizing complex numbers (real=price, imag=volume)."""

    @staticmethod
    def pack(price: float, volume: float) -> complex:
        return complex(price, volume)

    @staticmethod
    def unpack(tick: complex) -> Tuple[float, float]:
        return tick.real, tick.imag


def compute_vwap_vectorized(ticks: List[Tuple[float, float]]) -> float:
    """Calculates VWAP using complex inner-product mechanics."""
    if not ticks:
        return 0.0
    complex_stream = [ComplexTicker.pack(p, v) for p, v in ticks]
    total_vol = sum(t.imag for t in complex_stream)
    if total_vol == 0:
        return 0.0
    weighted_sum = sum(t.real * t.imag for t in complex_stream)
    return round(weighted_sum / total_vol, 8)


def normalize_ohlcv_batch(
    raw_candles: List[Dict[str, Union[str, float]]]
) -> Generator[Dict[str, Union[str, float]], None, None]:
    """Generator normalizing raw candle data with dynamic log-return scaling."""
    prev_close = None
    for candle in raw_candles:
        symbol = str(candle.get("symbol", "BTC/USD")).upper()
        close_p = float(candle.get("close", 0.0))
        high_p = float(candle.get("high", close_p))
        low_p = float(candle.get("low", close_p))
        volume = float(candle.get("volume", 0.0))

        log_return = (
            math.log(close_p / prev_close) if prev_close and prev_close > 0 else 0.0
        )
        prev_close = close_p

        spread = max(high_p - low_p, 0.0)
        volatility_rad = math.atan2(spread, close_p) if close_p > 0 else 0.0

        yield {
            "symbol": symbol,
            "close": round(close_p, 4),
            "volume": round(volume, 2),
            "log_return": round(log_return, 6),
            "volatility": round(volatility_rad, 6),
        }
