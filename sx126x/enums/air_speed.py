from enum import Enum


class AirSpeed(Enum):
    K0_3 = 0.3
    K1_2 = 1.2
    K2_4 = 2.4
    K4_8 = 4.8
    K9_6 = 9.6
    K19_2 = 19.2
    K38_4 = 38.4
    K62_5 = 62.5

    @staticmethod
    def from_data(data: int) -> "AirSpeed":
        bits = data & 0b00000111
        if bits == 0b000:
            return AirSpeed.K0_3
        elif bits == 0b001:
            return AirSpeed.K1_2
        elif bits == 0b010:
            return AirSpeed.K2_4
        elif bits == 0b011:
            return AirSpeed.K4_8
        elif bits == 0b100:
            return AirSpeed.K9_6
        elif bits == 0b101:
            return AirSpeed.K19_2
        elif bits == 0b110:
            return AirSpeed.K38_4
        elif bits == 0b111:
            return AirSpeed.K62_5
        else:
            raise ValueError(f"Invalid air speed bits: {bits:03b}")

    def apply_to(self, data: int) -> int:
        if self == AirSpeed.K0_3:
            bits = 0b000
        elif self == AirSpeed.K1_2:
            bits = 0b001
        elif self == AirSpeed.K2_4:
            bits = 0b010
        elif self == AirSpeed.K4_8:
            bits = 0b011
        elif self == AirSpeed.K9_6:
            bits = 0b100
        elif self == AirSpeed.K19_2:
            bits = 0b101
        elif self == AirSpeed.K38_4:
            bits = 0b110
        elif self == AirSpeed.K62_5:
            bits = 0b111
        else:
            raise ValueError(f"Unsupported air speed: {self}")

        return (data & 0b11111000) | bits
