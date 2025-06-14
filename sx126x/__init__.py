from sx126x.sx126x import SX126X
from sx126x.enums import *
from sx126x.models import *

__version__ = "2.1.0"  # Keep in sync with pyproject.toml

__all__ = [
    "SX126X",
    "AirSpeed",
    "AmbientNoise",
    "BaudRate",
    "Command",
    "LBT",
    "Mode",
    "PacketSize",
    "Parity",
    "Register",
    "Relay",
    "RSSI",
    "TransferMethod",
    "TransmitPower",
    "WORControl",
    "WORPeriod",
    "Address",
    "CryptKey",
]
