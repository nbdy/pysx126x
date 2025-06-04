from enum import IntEnum


class TransmitPower(IntEnum):
    DBM_22 = 22
    DBM_17 = 17
    DBM_13 = 13
    DBM_10 = 10

    @staticmethod
    def from_data(data: int) -> "TransmitPower":
        bits = data & 0b00000011
        if bits == 0b00:
            return TransmitPower.DBM_22
        elif bits == 0b01:
            return TransmitPower.DBM_17
        elif bits == 0b10:
            return TransmitPower.DBM_13
        elif bits == 0b11:
            return TransmitPower.DBM_10
        else:
            raise ValueError(f"Invalid transmit power bits: {bits:02b}")

    def apply_to(self, data: int) -> int:
        if self == TransmitPower.DBM_22:
            bits = 0b00
        elif self == TransmitPower.DBM_17:
            bits = 0b01
        elif self == TransmitPower.DBM_13:
            bits = 0b10
        elif self == TransmitPower.DBM_10:
            bits = 0b11
        else:
            raise ValueError(f"Unsupported transmit power: {self}")

        return (data & 0b11111100) | bits
