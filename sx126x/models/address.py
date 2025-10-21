from dataclasses import dataclass


def parse_address(addr: str) -> tuple[int, int]:
    parts = addr.split(".")
    if len(parts) != 2:
        raise ValueError("Address must be in format 'H.L', (decimal)")
    return int(parts[0]), int(parts[1])


@dataclass
class Address:
    hi: int
    lo: int

    @staticmethod
    def parse(addr: str) -> "Address":
        return Address(*parse_address(addr))

    def __str__(self):
        return f"{self.hi}.{self.lo}"

    @classmethod
    def from_int(cls, val: int) -> "Address":
        return cls((val >> 8), val & 0xFF)

    def to_bytes(self) -> bytes:
        return bytes([self.hi, self.lo])
