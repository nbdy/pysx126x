from enum import IntEnum


class Command(IntEnum):
    WRITE = 0xC0
    READ = 0xC1
    WRITE_TEMP = 0xC2
    WIRELESS_CFG = 0xCF
