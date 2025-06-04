from enum import Enum


class Relay(Enum):
    DISABLED = 0
    ENABLED = 1

    @staticmethod
    def from_data(data: int) -> "Relay":
        return Relay((data >> 5) & 0b1)

    def apply_to(self, data: int) -> int:
        return (data & 0b11011111) | (self.value << 5)
