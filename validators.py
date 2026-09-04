import re
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ValidationResult:
    is_valid: bool
    error: Optional[str] = None

class CryptoInputValidator:
    """Sanity checks for crypto ticker symbols and price payloads."""
    
    def __init__(self, allowed_quotes={"USD", "EUR", "BTC"}):
        self.allowed_quotes = allowed_quotes
        self.ticker_pattern = re.compile(r'^[A-Z]{2,6}$')

    def validate_ticker(self, ticker: Any) -> ValidationResult:
        if not isinstance(ticker, str):
            return ValidationResult(False, "Ticker must be a string")
        if not self.ticker_pattern.match(ticker):
            return ValidationResult(False, "Invalid ticker format")
        return ValidationResult(True)

    def validate_price(self, price: Any) -> ValidationResult:
        try:
            val = float(price)
            if val <= 0:
                return ValidationResult(False, "Price must be positive")
        except (ValueError, TypeError):
            return ValidationResult(False, "Price must be a numeric value")
        return ValidationResult(True)

    def run_check(self, data: dict) -> ValidationResult:
        ticker_check = self.validate_ticker(data.get('symbol'))
        if not ticker_check.is_valid:
            return ticker_check
            
        price_check = self.validate_price(data.get('price'))
        if not price_check.is_valid:
            return price_check
            
        return ValidationResult(True)