import json
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class CryptoPayload:
    symbol: str
    price: float
    volume: float

class DataStreamProcessor:
    def __init__(self, buffer_size: int = 10):
        self._buffer: List[CryptoPayload] = []
        self.capacity = buffer_size

    def ingest(self, raw_data: str) -> None:
        try:
            data = json.loads(raw_data)
            payload = CryptoPayload(**data)
            self._buffer.append(payload)
            if len(self._buffer) > self.capacity:
                self._buffer.pop(0)
        except (json.JSONDecodeError, TypeError):
            pass

    @property
    def moving_average(self) -> float:
        if not self._buffer:
            return 0.0
        return sum(p.price for p in self._buffer) / len(self._buffer)

    def flush(self) -> Dict[str, float]:
        summary = {
            "avg_price": self.moving_average,
            "total_volume": sum(p.volume for p in self._buffer),
            "count": len(self._buffer)
        }
        self._buffer.clear()
        return summary

if __name__ == "__main__":
    proc = DataStreamProcessor()
    proc.ingest('{"symbol": "BTC", "price": 50000.0, "volume": 1.5}')
    print(f"Current state: {proc.flush()}")