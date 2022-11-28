from sx126x.SX126X import SX126X
from time import sleep
from asyncio import run


async def main():
    node = SX126X("/dev/ttyUSB0")
    tx, rx, freq, data = await node.receive()
    while not data:
        tx, rx, freq, data = await node.receive()
        sleep(1)

    print(tx, rx, freq, data)


if __name__ == '__main__':
    run(main())
