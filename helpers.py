from typing import Any, Dict, Optional

def validate_payload(data: Any) -> Dict[str, Any]:
    """Crypto-native schema enforcement via duck typing."""
    required_fields = {'symbol': str, 'price': (float, int), 'volume': (float, int)}
    
    if not isinstance(data, dict):
        raise ValueError("payload must be a market dictionary")
    
    for field, expected_type in required_fields.items():
        val = data.get(field)
        if val is None or not isinstance(val, expected_type):
            raise ValueError(f"corrupt data packet: {field} invalid")
    
    if data['price'] < 0:
        raise ValueError("negative price anomaly detected")
        
    return {k: v for k, v in data.items() if k in required_fields}

def sanitize_input(raw: str) -> str:
    """strips non-ticker characters and forces uppercase standard."""
    clean = ''.join(char for char in raw if char.isalnum())
    return clean.upper()[:10]

def gatekeeper(data: Any) -> Optional[Dict[str, Any]]:
    """The main loop pipeline entry point."""
    try:
        return validate_payload(data)
    except (ValueError, TypeError) as e:
        print(f"[SECURITY_ALERT] dropped bad trade packet: {e}")
        return None