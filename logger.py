import sys
import time
import collections

class PerformanceLogger:
    def __init__(self, window_size=100):
        self.history = collections.deque(maxlen=window_size)
        self._start_times = {}

    def track(self, event_id):
        self._start_times[event_id] = time.perf_counter()

    def flush(self, event_id):
        if event_id in self._start_times:
            duration = time.perf_counter() - self._start_times.pop(event_id)
            self.history.append(duration)

    def get_latency_stats(self):
        if not self.history:
            return 0.0
        return sum(self.history) / len(self.history)

# Singleton pattern for global stats aggregation
stats = PerformanceLogger()

def log_performance(func):
    def wrapper(*args, **kwargs):
        eid = f"{func.__name__}_{id(args)}"
        stats.track(eid)
        try:
            return func(*args, **kwargs)
        finally:
            stats.flush(eid)
    return wrapper

def report():
    avg = stats.get_latency_stats()
    sys.stderr.write(f'[METRIC] Crypto performance: {avg:.6f}s latency\n')
    return avg