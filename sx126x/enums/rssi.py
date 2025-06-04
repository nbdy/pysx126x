from enum import Enum


class RSSI(Enum):
    DISABLED = 0
    ENABLED = 1

    @staticmethod
    def from_data(data: int) -> "RSSI":
        return RSSI((data >> 7) & 0b1)

    def apply_to(self, data: int) -> int:
        return (data & 0b01111111) | (self.value << 7)
