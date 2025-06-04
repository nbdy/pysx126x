from enum import Enum


class TransferMethod(Enum):
    TRANSPARENT = 0
    FIXED = 1

    @staticmethod
    def from_data(data: int) -> "TransferMethod":
        return TransferMethod((data >> 6) & 0b1)

    def apply_to(self, data: int) -> int:
        return (data & 0b10111111) | (self.value << 6)
