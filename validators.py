import re
from typing import Any

class CryptoValidator:
    def __init__(self, patterns: dict = None):
        self._patterns = patterns or {
            "ticker": r"^[A-Z]{2,6}$",
            "address": r"^0x[a-fA-F0-9]{40}$"
        }

    def __call__(self, key: str, value: Any) -> bool:
        pattern = self._patterns.get(key)
        if not pattern:
            return True
        return bool(re.match(pattern, str(value)))

    @staticmethod
    def strict_check(data: dict, schema: dict) -> bool:
        return all(
            isinstance(data.get(k), v) for k, v in schema.items()
        )

def validate_payload(data: dict) -> bool:
    validator = CryptoValidator()
    checks = [
        validator("ticker", data.get("symbol")), 
        validator("address", data.get("wallet"))
    ]
    return all(checks)

if __name__ == "__main__":
    sample = {"symbol": "BTC", "wallet": "0x1234567890abcdef1234567890abcdef12345678"}
    print(f"Validation status: {validate_payload(sample)}")