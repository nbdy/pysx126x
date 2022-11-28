from sx126x.SX126X import SX126X
from asyncio import run


async def main():
    node = SX126X("/dev/ttyUSB1", 2)
    await node.send_to(1, 868, b"Hello\0")


if __name__ == '__main__':
    run(main())
