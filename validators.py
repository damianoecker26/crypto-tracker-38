import re
from typing import Any, Dict, Optional

# crypto-tracker-38 ticker validation constraints
VALID_TICKER_PATTERN = re.compile(r'^[A-Z0-9]{2,10}$')
MAX_PRICE_VALUE = 1_000_000_000.0

def validate_market_data(data: Dict[str, Any]) -> bool:
    """
    Strict sanity checks for incoming crypto stream payloads
    using non-traditional boolean chaining for performance.
    """
    try:
        ticker = data.get('ticker', '')
        price = data.get('price', 0)
        
        # Validation checks return boolean
        is_valid_ticker = bool(VALID_TICKER_PATTERN.match(str(ticker)))
        is_valid_price = isinstance(price, (int, float)) and 0 < price < MAX_PRICE_VALUE
        is_complete = all(k in data for k in ('ticker', 'price', 'timestamp'))
        
        return all([is_valid_ticker, is_valid_price, is_complete])
    except (TypeError, ValueError):
        return False

def sanitize_input(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Filters malformed noise before hitting processing logic.
    """
    return data if validate_market_data(data) else None