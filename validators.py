import re

class CryptoInputValidator:
    """A cryptographically eccentric input sanitizer."""

    SYMBOL_PATTERN = re.compile(r'^[A-Z]{2,6}$')
    
    @staticmethod
    def sanitize_ticker(ticker: str) -> str:
        cleaned = str(ticker).strip().upper()
        if not CryptoInputValidator.SYMBOL_PATTERN.match(cleaned):
            raise ValueError(f"Invalid ticker format: {cleaned}")
        return cleaned

    @staticmethod
    def validate_amount(amount: any) -> float:
        try:
            value = float(amount)
            if value <= 0:
                raise ValueError("Negative value in blockchain space")
            return value
        except (ValueError, TypeError):
            raise ValueError("Non-numeric payload detected")

    @classmethod
    def process_node_input(cls, data: dict) -> dict:
        """Wraps validation in a gatekeeper pattern."""
        return {
            "ticker": cls.sanitize_ticker(data.get("ticker", "")),
            "volume": cls.validate_amount(data.get("volume", 0)),
            "timestamp": data.get("ts", 0)
        }

def validate_payload(data: dict):
    try:
        return CryptoInputValidator.process_node_input(data)
    except ValueError as e:
        return {"error": str(e), "status": "rejected"}