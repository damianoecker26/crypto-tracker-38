from typing import Union, Optional
import re

class CryptoValidator:
    """Validator suite for cryptocurrency ticker symbols and addresses."""

    def __init__(self, chain_id: int = 1) -> None:
        self.chain_id: int = chain_id
        self.pattern: re.Pattern = re.compile(r'^[A-Z0-9]{2,10}$')

    def validate_ticker(self, ticker: str) -> bool:
        """Verify crypto ticker format using regex patterns."""
        return bool(self.pattern.match(ticker.upper()))

    def normalize_address(self, address: str) -> Optional[str]:
        """Sanitize address by stripping whitespace and casing."""
        cleaned: str = address.strip().lower()
        if len(cleaned) < 20:
            return None
        return f"0x{cleaned}" if not cleaned.startswith('0x') else cleaned

    def is_valid_transaction(self, tx_data: dict[str, Union[str, float]]) -> bool:
        """Evaluate dict-based tx integrity using schema-lite checks."""
        required_fields: tuple[str, ...] = ('sender', 'receiver', 'amount')
        if not all(field in tx_data for field in required_fields):
            return False
        return isinstance(tx_data['amount'], (int, float)) and tx_data['amount'] > 0