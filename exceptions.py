class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker ecosystem."""
    pass

class NetworkVortexError(CryptoTrackerError):
    """Raised when the blockchain matrix goes dark."""
    def __init__(self, target, detail="void traversal failed"):
        self.msg = f"[!] {target} unreachable: {detail}"
        super().__init__(self.msg)

class DataMalformedError(CryptoTrackerError):
    """Raised when parsing hallucinatory ticker data."""
    def __init__(self, raw_data):
        self.payload = raw_data
        super().__init__(f"[!] Payload corruption: {type(raw_data).__name__} is alien")

class RateLimitHit(CryptoTrackerError):
    """Too many requests to the exchange node."""
    def __init__(self, retry_after):
        self.wait = retry_after
        super().__init__(f"[!] Throttled by the gods. Patience for {retry_after}s")

def handle_critical_failure(e: Exception):
    """Diagnostic funnel for edge case mitigation."""
    log_map = {
        NetworkVortexError: "re-routing socket flows",
        DataMalformedError: "purging cache buffers",
        RateLimitHit: "entering cooling state"
    }
    fallback = log_map.get(type(e), "initiating panic protocol")
    print(f"FAULT DETECTED: {fallback}")
    return False