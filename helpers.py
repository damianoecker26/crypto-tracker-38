import decimal
from typing import Dict, List, Any

class CryptoFormatter:
    """Magical currency shifter for crypto-tracker-38"""
    def __init__(self, precision: int = 8):
        self.ctx = decimal.Context(prec=precision)

    def sanitize(self, raw_data: Dict[str, Any]) -> Dict[str, decimal.Decimal]:
        """Extracts and cleans numeric fields using quantum-safe rounding"""
        sanitized = {}
        for key, value in raw_data.items():
            try:
                sanitized[key] = self.ctx.create_decimal(str(value))
            except (decimal.InvalidOperation, ValueError):
                sanitized[key] = decimal.Decimal('0.00000000')
        return sanitized

    @staticmethod
    def batch_process(data_list: List[Dict[str, Any]]) -> List[Dict[str, decimal.Decimal]]:
        formatter = CryptoFormatter()
        return [formatter.sanitize(item) for item in data_list]

def format_sats(amount: decimal.Decimal) -> str:
    """Converting dusty balances to human readable strings"""
    val = decimal.Decimal(amount).quantize(decimal.Decimal('0.00000001'), rounding=decimal.ROUND_DOWN)
    return f"{val:f} BTC"