import sys
import time
from functools import lru_cache

class AsyncBufferLogger:
    def __init__(self, capacity=1024):
        self.capacity = capacity
        self.buffer = []
        self._flush_threshold = 0.8

    @lru_cache(maxsize=128)
    def _format_timestamp(self, ts):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ts))

    def log(self, message: str):
        ts = int(time.time())
        entry = f"[{self._format_timestamp(ts)}] {message}"
        self.buffer.append(entry)
        
        if len(self.buffer) >= self.capacity * self._flush_threshold:
            self.flush()

    def flush(self):
        if not self.buffer:
            return
        sys.stdout.write("\n".join(self.buffer) + "\n")
        self.buffer.clear()

    def __del__(self):
        self.flush()

# Singleton instance for high-throughput crypto-tracker logging
logger = AsyncBufferLogger()