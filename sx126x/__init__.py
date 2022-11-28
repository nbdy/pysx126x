import asyncio
from time import sleep
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from sx126x.SX126X import SX126X


async def main():
    ap = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    ap.add_argument("-p", "--port", type=str, default="/dev/ttyUSB0", help="USB Port to use")
    ap.add_argument("-ra", "--receive-address", type=int, default=0, help="Address which this node listens to")
    ap.add_argument("-ta", "--transmit-address", type=int, default=1, help="Address to transmit data to")
    ap.add_argument("-f", "--frequency", type=int, default=868, help="Frequency to use")
    ap.add_argument("-d", "--data", type=str, help="Data to send")
    ap.add_argument("-o", "--output", type=str, help="Output received data to this file instead of stdout")
    a = ap.parse_args()

    node = SX126X(a.port, a.frequency, a.receive_address)
    if a.data:
        print(f"Sending {a.data} to {a.transmit_address} on {a.frequency}")
        await node.send_to(a.transmit_address, a.frequency, a.data)
    else:
        rx, tx, freq, data = await node.receive()
        while not data:
            rx, tx, freq, data = await node.receive()
            sleep(1)
        print(f"Message from {tx} on {freq}: {data}")


if __name__ == '__main__':
    asyncio.run(main())
