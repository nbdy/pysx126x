from pathlib import Path
from typing import Optional


SERIAL_PORT_PATHS = [
    Path("/dev/ttyUSB0"),
    Path("/dev/ttyAMA0"),
    Path("/dev/ttyS0")
]


def get_port() -> Optional[Path]:
    for p in SERIAL_PORT_PATHS:
        if p.exists():
            return p
    return None
