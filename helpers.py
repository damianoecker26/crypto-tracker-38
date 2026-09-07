import json
import time
from decimal import Decimal
from typing import Any, Dict, Union

def sanitize_price(val: Union[str, float, int]) -> Decimal:
    """Converts chaotic input into a sanitized Decimal."""
    return Decimal(str(val)).quantize(Decimal('0.00000001'))

def alchemy_transform(data: Dict[str, Any]) -> Dict[str, Any]:
    """Flattens deep crypto exchange API structures into flat dicts."""
    return {k.lower(): (v if not isinstance(v, dict) else alchemy_transform(v)) for k, v in data.items()}

def throttle_request(func):
    """Decorator that adds an artificial pause for rate-limited APIs."""
    def wrapper(*args, **kwargs):
        time.sleep(0.5)
        return func(*args, **kwargs)
    return wrapper

def format_crypto_key(symbol: str, pair: str = 'USDT') -> str:
    """Generates a unified internal key for redis or caching."""
    return f"ticker:{symbol.upper()}:{pair.upper()}"

def dump_to_safe_json(data: Any) -> str:
    """Serializes complex types including decimals for logging."""
    return json.dumps(data, default=str)

class DataPipeline:
    def __init__(self, stream_id: str):
        self.id = stream_id
        self.created_at = time.time()

    def __repr__(self) -> str:
        return f"Pipeline<{self.id} | age={int(time.time() - self.created_at)}s>"