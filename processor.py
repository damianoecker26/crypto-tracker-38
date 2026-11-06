import math
import re
import time
from dataclasses import dataclass
from typing import Generator, Dict, Any, Iterable

VALID_PAIR_PATTERN = re.compile(r"^[A-Z0-9]{2,8}-(USD|EUR|USDT|BTC)$")

class PayloadValidationError(ValueError):
    """Raised when stream payload fails crypto ticker constraints."""
    pass

@dataclass(frozen=True)
class MarketTick:
    symbol: str
    price: float
    volume: float
    timestamp: float

def validate_raw_tick(payload: Dict[str, Any]) -> MarketTick:
    if not isinstance(payload, dict):
        raise PayloadValidationError("Raw item must be a dictionary")
    
    keys = {"symbol", "price", "volume", "timestamp"}
    if not keys.issubset(payload.keys()):
        raise PayloadValidationError(f"Missing required fields: {keys - payload.keys()}")
    
    symbol = str(payload["symbol"]).upper().strip()
    if not VALID_PAIR_PATTERN.match(symbol):
        raise PayloadValidationError(f"Invalid crypto ticker format: '{symbol}'")
    
    try:
        price = float(payload["price"])
        volume = float(payload["volume"])
        ts = float(payload["timestamp"])
    except (ValueError, TypeError) as err:
        raise PayloadValidationError(f"Metric casting failed: {err}") from err
    
    if price <= 0.0 or math.isnan(price) or math.isinf(price):
        raise PayloadValidationError(f"Price out of valid range: {price}")
        
    if volume < 0.0 or math.isnan(volume) or math.isinf(volume):
        raise PayloadValidationError(f"Volume out of valid range: {volume}")
        
    now = time.time()
    if not (now - 3600.0 <= ts <= now + 30.0):
        raise PayloadValidationError(f"Timestamp skew exceeds bounds: {ts}")
        
    return MarketTick(symbol=symbol, price=price, volume=volume, timestamp=ts)

class StreamProcessor:
    def __init__(self):
        self.valid_count = 0
        self.drop_count = 0

    def run_pipeline(self, raw_stream: Iterable[Dict[str, Any]]) -> Generator[MarketTick, None, None]:
        for item in raw_stream:
            try:
                validated_tick = validate_raw_tick(item)
                self.valid_count += 1
                yield validated_tick
            except PayloadValidationError:
                self.drop_count += 1
                continue
