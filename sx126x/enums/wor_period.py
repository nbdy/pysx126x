from enum import Enum


class WORPeriod(Enum):
    MS_500 = 0
    MS_1000 = 1
    MS_1500 = 2
    MS_2000 = 3
    MS_2500 = 4
    MS_3000 = 5
    MS_3500 = 6
    MS_4000 = 7

    @staticmethod
    def from_data(data: int) -> "WORPeriod":
        return WORPeriod(data & 0b00000111)

    def apply_to(self, data: int) -> int:
        return (data & 0b11111000) | (self.value & 0b00000111)
