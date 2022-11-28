# sx126x

## install

```shell
pip3 install sx126x
```

## example

## receiver

```python
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
```

## sender

```python
from sx126x.SX126X import SX126X
from asyncio import run


async def main():
    node = SX126X("/dev/ttyUSB1", 2)
    await node.send_to(1, 868, b"Hello\0")


if __name__ == '__main__':
    run(main())
```
