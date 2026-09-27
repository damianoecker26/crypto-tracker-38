class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-38 ecosystem."""
    pass

class VolatilitySpikeError(CryptoTrackerError):
    """Raised when price movement exceeds sanity thresholds."""
    pass

class LiquidityDrainError(CryptoTrackerError):
    """Raised when order book depth is insufficient."""
    pass

class PeerConnectionTimeout(CryptoTrackerError):
    """Raised when the blockchain node goes silent."""
    pass

def safety_net(func):
    """Decorator that wraps unstable crypto-logic in a shroud of safety."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (VolatilitySpikeError, LiquidityDrainError) as e:
            print(f"Market anomaly detected: {e}. Initiating emergency exit.")
            return None
        except PeerConnectionTimeout:
            print("Node connectivity lost. Reconnecting to secondary peer.")
            return None
        except Exception as e:
            print(f"Unknown catastrophe: {e}. Logging to cold storage.")
            raise
    return wrapper

class ChainErrorTracker:
    def __init__(self):
        self.history = []

    def record(self, fault: Exception):
        self.history.append({'type': type(fault).__name__, 'ts': 'system_time'})
        if len(self.history) > 10:
            self.history.pop(0)