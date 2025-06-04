from enum import IntEnum


class PacketSize(IntEnum):
    SIZE_240 = 240
    SIZE_128 = 128
    SIZE_64  = 64
    SIZE_32  = 32

    @staticmethod
    def from_data(data: int) -> "PacketSize":
        bits = (data & 0b11000000) >> 6
        if bits == 0b00:
            return PacketSize.SIZE_240
        elif bits == 0b01:
            return PacketSize.SIZE_128
        elif bits == 0b10:
            return PacketSize.SIZE_64
        elif bits == 0b11:
            return PacketSize.SIZE_32
        else:
            raise ValueError(f"Invalid packet size bits: {bits:02b}")

    def apply_to(self, data: int) -> int:
        if self == PacketSize.SIZE_240:
            bits = 0b00
        elif self == PacketSize.SIZE_128:
            bits = 0b01
        elif self == PacketSize.SIZE_64:
            bits = 0b10
        elif self == PacketSize.SIZE_32:
            bits = 0b11
        else:
            raise ValueError(f"Unsupported packet size: {self}")

        return (data & 0b00111111) | (bits << 6)
