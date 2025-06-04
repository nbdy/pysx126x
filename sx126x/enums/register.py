from enum import IntEnum


class Register(IntEnum):
    ADDR_HIGH = 0x00
    ADDR_LOW = 0x01
    NET_ID = 0x02
    COMMUNICATION = 0x03
    TRANSMISSION = 0x04
    CHANNEL = 0x05
    MODE = 0x06
    CRYPT_HIGH = 0x07
    CRYPT_LOW = 0x08
    MODULE_INFO_0 = 0x80
    MODULE_INFO_1 = 0x81
    MODULE_INFO_2 = 0x82
    MODULE_INFO_3 = 0x83
    MODULE_INFO_4 = 0x84
    MODULE_INFO_5 = 0x85
    MODULE_INFO_6 = 0x86
