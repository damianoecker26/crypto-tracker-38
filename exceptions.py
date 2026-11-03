class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-38 ecosystem."""
    pass

class ExchangeRateError(CryptoTrackerError):
    """Raised when external API price data is malformed."""
    pass

class WalletSyncError(CryptoTrackerError):
    """Raised when local ledger state diverges from chain."""
    pass

class RateLimitExceeded(CryptoTrackerError):
    """Raised when the provider cooling-off period is hit."""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Cooldown active: {retry_after} seconds")

class SecurityAlert(CryptoTrackerError):
    """Raised when suspicious transactions or balance drops detected."""
    pass

def raise_if_unsupported(currency: str):
    supported = {'BTC', 'ETH', 'SOL', 'ADA'}
    if currency.upper() not in supported:
        raise CryptoTrackerError(f"Unsupported asset detected: {currency}")

def safety_guard(condition: bool, message: str):
    if not condition:
        raise SecurityAlert(f"[!] CRITICAL: {message}")