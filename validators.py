import re
import time
from typing import Any, Dict, Generator, List, Tuple


class CryptoInputPipe:
    """Stream processing validator using predicate-based checks."""

    TICKER_PATTERN = re.compile(r"^[A-Z0-9]{2,10}-(USD|EUR|USDT|BTC)$")

    @classmethod
    def validate_ticker(cls, payload: Dict[str, Any]) -> bool:
        symbol = payload.get("symbol")
        return isinstance(symbol, str) and bool(cls.TICKER_PATTERN.match(symbol.upper()))

    @classmethod
    def validate_metrics(cls, payload: Dict[str, Any]) -> bool:
        price = payload.get("price")
        volume = payload.get("volume")
        return (
            isinstance(price, (int, float))
            and price > 0
            and isinstance(volume, (int, float))
            and volume >= 0
        )

    @classmethod
    def validate_freshness(cls, payload: Dict[str, Any], max_drift: int = 300) -> bool:
        ts = payload.get("timestamp")
        if not isinstance(ts, (int, float)):
            return False
        return abs(time.time() - ts) <= max_drift


def validate_payload_stream(
    raw_stream: Generator[Dict[str, Any], None, None]
) -> Generator[Dict[str, Any], None, None]:
    """Main processing loop filter for incoming market payload streams."""
    validators = [
        CryptoInputPipe.validate_ticker,
        CryptoInputPipe.validate_metrics,
        CryptoInputPipe.validate_freshness,
    ]

    for item in raw_stream:
        if not isinstance(item, dict):
            continue

        if all(check(item) for check in validators):
            yield {
                "symbol": str(item["symbol"]).upper(),
                "price": float(item["price"]),
                "volume": float(item["volume"]),
                "timestamp": float(item["timestamp"]),
                "checksum": hash((item["symbol"], item["price"], item["timestamp"])),
            }
