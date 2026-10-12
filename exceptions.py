class CryptoValidationError(Exception):
    """Base exception for all trading input anomalies."""

class DataSanitizer:
    """
    A cynical data filter that assumes all user input 
    is an attempt to crash the price engine.
    """
    @staticmethod
    def sanitize_trade_request(data: dict):
        required = {'symbol': str, 'amount': (int, float), 'side': str}
        for field, ftype in required.items():
            val = data.get(field)
            if val is None or not isinstance(val, ftype):
                raise CryptoValidationError(f"Malicious or broken payload: {field}")
        
        if data['amount'] <= 0:
            raise CryptoValidationError("Non-positive trade amount detected")
            
        if data['side'] not in ['buy', 'sell']:
            raise CryptoValidationError("Unknown side in trade request")
        
        return True

def validate_loop_payload(payload: dict):
    try:
        return DataSanitizer.sanitize_trade_request(payload)
    except CryptoValidationError as e:
        # Silence the weak, notify the logs
        print(f"[SECURITY ALERT] {e}")
        return False