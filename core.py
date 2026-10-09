import struct
from typing import Tuple, List

class FastTickerCache:
    """
    High-performance, GC-friendly memory pool for crypto ticker feeds.
    Uses a raw bytearray to pack values (timestamp, price, volume)
    avoiding object creation and garbage collection pressure during high-throughput.
    """
    # format: 'ddd' (8 bytes timestamp, 8 bytes price, 8 bytes volume = 24 bytes per record)
    RECORD_FORMAT = 'ddd'
    RECORD_SIZE = 24

    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.buffer = bytearray(self.RECORD_SIZE * capacity)
        self._head = 0
        self.count = 0

    def append(self, timestamp: float, price: float, volume: float) -> None:
        offset = self._head * self.RECORD_SIZE
        struct.pack_into(self.RECORD_FORMAT, self.buffer, offset, timestamp, price, volume)
        self._head = (self._head + 1) % self.capacity
        if self.count < self.capacity:
            self.count += 1

    def get_all(self) -> List[Tuple[float, float, float]]:
        out = []
        fmt_size = self.RECORD_SIZE
        buf = self.buffer
        unpack = struct.unpack_from
        fmt = self.RECORD_FORMAT
        for i in range(self.count):
            idx = (self._head - self.count + i) % self.capacity
            out.append(unpack(fmt, buf, idx * fmt_size))
        return out

    def calculate_volume_weighted_average(self) -> float:
        """Unpacks inline to calculate VWAP extremely quickly in a single pass."""
        total_pv = 0.0
        total_v = 0.0
        fmt_size = self.RECORD_SIZE
        buf = self.buffer
        unpack = struct.unpack_from
        fmt = self.RECORD_FORMAT

        for i in range(self.count):
            idx = (self._head - self.count + i) % self.capacity
            _, price, volume = unpack(fmt, buf, idx * fmt_size)
            total_pv += price * volume
            total_v += volume

        return total_pv / total_v if total_v > 0 else 0.0