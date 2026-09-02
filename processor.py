import json
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CryptoEntry:
    symbol: str
    price: float
    volume: float

def is_valid_symbol(symbol: str) -> bool:
    return bool(symbol) and symbol.isalpha() and symbol.isupper() and 3 <= len(symbol) <= 5

def validate_input(entry: dict) -> Optional[CryptoEntry]:
    if not isinstance(entry, dict):
        return None
    try:
        symbol = str(entry.get("symbol", "")).strip().upper()
        if not is_valid_symbol(symbol):
            return None
        price = float(entry.get("price", 0))
        if price <= 0:
            return None
        volume = float(entry.get("volume", 0))
        if volume < 0:
            return None
        return CryptoEntry(symbol=symbol, price=price, volume=volume)
    except (ValueError, TypeError, AttributeError):
        return None

def main_processing_loop(raw_inputs: List[dict]) -> List[CryptoEntry]:
    validated_entries = []
    for raw in raw_inputs:
        basic_checks = (
            isinstance(raw, dict),
            "symbol" in raw,
            "price" in raw
        )
        if not all(basic_checks):
            continue
        entry = validate_input(raw)
        if entry is not None:
            processed_entry = CryptoEntry(
                symbol=entry.symbol,
                price=round(entry.price, 2),
                volume=entry.volume
            )
            validated_entries.append(processed_entry)
    return validated_entries

if __name__ == "__main__":
    sample_data = [
        {"symbol": "BTC", "price": 67234.567, "volume": 12345.67},
        {"symbol": "ETH", "price": 3456.78, "volume": 9876},
        {"symbol": "xrp", "price": 0.52, "volume": 50000},
        {"symbol": "ADA", "price": 0.45, "volume": -100},
        {"symbol": "SOL", "price": 150, "volume": 8000},
        {"symbol": "TOO LONG", "price": 10, "volume": 100},
        {"symbol": "BTC", "price": "invalid", "volume": 100},
        12345
    ]
    results = main_processing_loop(sample_data)
    print(json.dumps([{"symbol": e.symbol, "price": e.price, "volume": e.volume} for e in results], indent=2))