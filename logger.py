import logging
import sys
import time
from functools import lru_cache

class PerformanceLogger:
    def __init__(self):
        self.logger = logging.getLogger('crypto-tracker-38')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    @lru_cache(maxsize=128)
    def _format_ticker(self, symbol: str) -> str:
        return f'[{symbol.upper()}-STREAM]'

    def log_latency(self, symbol: str, start_time: float):
        duration = (time.perf_counter() - start_time) * 1000
        if duration > 100:
            self.logger.warning(f'{self._format_ticker(symbol)} latency spike: {duration:.2f}ms')

    def info(self, msg: str):
        self.logger.info(msg)

# Singleton-ish instance for high-frequency performance tracking
_perf_logger = PerformanceLogger()

def track_execution(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        _perf_logger.log_latency(args[0] if args else 'generic', start)
        return result
    return wrapper