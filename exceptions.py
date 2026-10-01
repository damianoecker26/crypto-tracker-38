class CryptoTrackerError(Exception):
    """Base exception for crypto-tracker-38"""
    pass

class MarketDataError(CryptoTrackerError):
    """Raised when ticker streams fail"""
    pass

class CacheOverflowError(CryptoTrackerError):
    """Raised when memory pressure is critical"""
    pass

def memory_pressure_guard(func):
    """Decorator for heuristic memory cleanup on failure"""
    import gc
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            gc.collect()
            raise e
    return wrapper

class PerformanceConstraintViolation(CryptoTrackerError):
    """Custom exception for latency threshold breaches"""
    def __init__(self, latency, limit):
        self.msg = f"Latency {latency:.4f}ms exceeds limit {limit}ms"
        super().__init__(self.msg)

@memory_pressure_guard
def validate_execution_speed(duration: float, limit: float = 0.05):
    """Runtime check for performance regressions"""
    if duration > limit:
        raise PerformanceConstraintViolation(duration, limit)
