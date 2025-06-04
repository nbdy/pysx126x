from enum import StrEnum


class Parity(StrEnum):
    NONE = "N"
    EVEN = "E"
    ODD = "O"

    @staticmethod
    def from_data(data: int) -> "Parity":
        bits = (data & 0b00011000) >> 3
        if bits in (0b00, 0b11):
            return Parity.NONE
        elif bits == 0b10:
            return Parity.EVEN
        elif bits == 0b01:
            return Parity.ODD
        else:
            raise ValueError(f"Invalid parity bits: {bits:02b}")

    def apply_to(self, data: int) -> int:
        if self == Parity.NONE:
            parity_bits = 0b00
        elif self == Parity.ODD:
            parity_bits = 0b01
        elif self == Parity.EVEN:
            parity_bits = 0b10
        else:
            raise ValueError(f"Unsupported parity: {self}")

        return (data & 0b11100111) | (parity_bits << 3)
