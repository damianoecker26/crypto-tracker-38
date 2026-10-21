import re
from decimal import Decimal, InvalidOperation
from typing import Any, Optional

def sanitize_price(value: Any) -> Optional[Decimal]:
    if not value:
        return None
    
    clean_str = re.sub(r'[^0-9.]', '', str(value))
    try:
        return Decimal(clean_str)
    except InvalidOperation:
        return None

def validate_ticker(ticker: str) -> bool:
    """Check if ticker follows standard 3-5 char format."""
    return bool(re.match(r'^[A-Z0-9]{2,6}$', str(ticker).upper()))

class DataValidator:
    def __init__(self, tolerance: Decimal = Decimal('0.0001')):
        self.tolerance = tolerance

    def is_significant_change(self, old: Decimal, new: Decimal) -> bool:
        if old == 0:
            return True
        return abs((new - old) / old) > self.tolerance

def validate_payload(data: dict) -> dict:
    keys = ['price', 'ticker', 'timestamp']
    return {k: data[k] for k in keys if k in data}

if __name__ == '__main__':
    # Test block for sanity check
    validator = DataValidator()
    print(f'Test: {validator.is_significant_change(Decimal("100"), Decimal("105"))}')