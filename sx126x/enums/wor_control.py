from enum import Enum


class WORControl(Enum):
    TRANSMIT = 0
    RECEIVE = 1

    @staticmethod
    def from_data(data: int) -> "WORControl":
        return WORControl((data >> 3) & 0b1)

    def apply_to(self, data: int) -> int:
        return (data & 0b11110111) | (self.value << 3)
