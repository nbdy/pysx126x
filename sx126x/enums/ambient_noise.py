from enum import Enum


class AmbientNoise(Enum):
    DISABLED = 0
    ENABLED = 1

    @staticmethod
    def from_data(data: int) -> "AmbientNoise":
        bit = (data & 0b00100000) >> 5
        return AmbientNoise.ENABLED if bit else AmbientNoise.DISABLED

    def apply_to(self, data: int) -> int:
        if self == AmbientNoise.ENABLED:
            modified_byte = data | 0b00100000  # Set bit 5
        elif self == AmbientNoise.DISABLED:
            modified_byte = data & 0b11011111  # Clear bit 5
        else:
            raise ValueError(f"Unsupported ambient noise setting: {self}")

        return modified_byte
