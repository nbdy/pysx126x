from dataclasses import dataclass


def parse_crypt_key(addr: str) -> tuple[int, int]:
    parts = addr.split(":")
    if len(parts) != 2:
        raise ValueError("Key must be in format 'H:L', (hex)")
    return int(parts[0], 16), int(parts[1], 16)


@dataclass
class CryptKey:
    hi: int
    lo: int

    @staticmethod
    def parse(key: str) -> "CryptKey":
        return CryptKey(*parse_crypt_key(key))

    def __str__(self):
        return f"{self.hi:X}:{self.lo:X}"

    @classmethod
    def from_data(cls, data: bytes) -> "CryptKey":
        if len(data) != 2:
            raise ValueError("Data must be 2 bytes")
        return cls(data[0], data[1])

    def to_bytes(self) -> bytes:
        return bytes([self.hi, self.lo])
