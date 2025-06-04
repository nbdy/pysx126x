from enum import IntEnum


class BaudRate(IntEnum):
    B1200 = 1200
    B2400 = 2400
    B4800 = 4800
    B9600 = 9600
    B19200 = 19200
    B38400 = 38400
    B57600 = 57600
    B115200 = 115200

    @staticmethod
    def from_data(data: int) -> "BaudRate":
        bits = (data & 0b11100000) >> 5
        bit_to_baud = {
            0b000: BaudRate.B1200,
            0b001: BaudRate.B2400,
            0b010: BaudRate.B4800,
            0b011: BaudRate.B9600,
            0b100: BaudRate.B19200,
            0b101: BaudRate.B38400,
            0b110: BaudRate.B57600,
            0b111: BaudRate.B115200,
        }
        try:
            return bit_to_baud[bits]
        except KeyError:
            raise ValueError(f"Invalid baud rate bits: {bits:03b}")

    def apply_to(self, data: int) -> int:
        baud_to_bits = {
            BaudRate.B1200: 0b000,
            BaudRate.B2400: 0b001,
            BaudRate.B4800: 0b010,
            BaudRate.B9600: 0b011,
            BaudRate.B19200: 0b100,
            BaudRate.B38400: 0b101,
            BaudRate.B57600: 0b110,
            BaudRate.B115200: 0b111,
        }
        bit_value = baud_to_bits[self] << 5
        cleared = data & 0b00011111
        return cleared | bit_value
