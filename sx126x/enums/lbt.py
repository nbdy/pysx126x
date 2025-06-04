from enum import Enum


class LBT(Enum):
    DISABLED = 0
    ENABLED = 1

    @staticmethod
    def from_data(data: int) -> "LBT":
        return LBT((data >> 4) & 0b1)

    def apply_to(self, data: int) -> int:
        return (data & 0b11101111) | (self.value << 4)
