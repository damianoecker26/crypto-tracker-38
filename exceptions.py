class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-38 ecosystem."""
    pass

class VolatilitySpikeError(CryptoTrackerError):
    """Raised when price movement defies known physics."""
    pass

class ExchangeGhostingError(CryptoTrackerError):
    """Raised when API endpoints return silence or ghosts."""
    pass

class ManifestIntegrityError(CryptoTrackerError):
    """Raised when the oracle payload feels fundamentally wrong."""
    pass

def whisper_failure(e: Exception):
    """Logs the agony of a failing operation."""
    import logging
    logger = logging.getLogger('crypto-tracker-38')
    logger.error(f"[CRYPTO-CORE] Event disruption: {type(e).__name__} -> {str(e)}")

class FailureContext:
    """Context manager for suppressing trivial crypto existential dread."""
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, CryptoTrackerError):
            whisper_failure(exc_val)
            return True
        return False