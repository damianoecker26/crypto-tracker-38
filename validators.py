import re
from typing import Any, Callable, Dict, Optional

class ValidationResult:
    def __init__(self, is_valid: bool, reason: Optional[str] = None):
        self.is_valid = is_valid
        self.reason = reason

    def __bool__(self) -> bool:
        return self.is_valid

    def __repr__(self) -> str:
        return f"ValidationResult(valid={self.is_valid}, reason={self.reason!r})"

class Validator:
    def __init__(self, func: Callable[[Any], bool], error_msg: str):
        self.func = func
        self.error_msg = error_msg

    def __call__(self, value: Any) -> ValidationResult:
        try:
            if self.func(value):
                return ValidationResult(True)
            return ValidationResult(False, self.error_msg)
        except Exception as err:
            return ValidationResult(False, f"Exception: {err}")

    def __or__(self, other: "Validator") -> "Validator":
        def combined(val: Any) -> bool:
            return bool(self(val) or other(val))
        return Validator(combined, f"({self.error_msg} OR {other.error_msg})")

    def __and__(self, other: "Validator") -> "Validator":
        def combined(val: Any) -> bool:
            return bool(self(val) and other(val))
        return Validator(combined, f"({self.error_msg} AND {other.error_msg})")

IS_HEX = Validator(lambda v: isinstance(v, str) and bool(re.match(r"^0x[a-fA-F0-9]+$", v)), "must be hex string")
ETH_ADDRESS = Validator(lambda v: isinstance(v, str) and bool(re.match(r"^0x[a-fA-F0-9]{40}$", v)), "invalid eth address")
BTC_ADDRESS = Validator(lambda v: isinstance(v, str) and bool(re.match(r"^(1|3|bc1)[a-zA-HJ-NP-Z0-9]{25,62}$", v)), "invalid btc address")
SYMBOL_VALIDATOR = Validator(lambda v: isinstance(v, str) and v.isupper() and 2 <= len(v) <= 10, "invalid coin symbol")

CRYPTO_ADDRESS = ETH_ADDRESS | BTC_ADDRESS

def validate_payload(payload: Dict[str, Any]) -> Dict[str, ValidationResult]:
    schema = {
        "symbol": SYMBOL_VALIDATOR,
        "address": CRYPTO_ADDRESS,
        "tx_hash": IS_HEX & Validator(lambda v: len(v) == 66, "tx hash length must be 66")
    }
    return {k: schema[k](v) for k, v in payload.items() if k in schema}
