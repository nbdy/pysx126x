from unittest import IsolatedAsyncioTestCase

from sx126x.SX126X import SX126X


class BasicTests(IsolatedAsyncioTestCase):
    async def test_send(self):
        node = SX126X("/dev/ttyUSB0")
        await node.send_to(1, 868, b"Hello")

    async def test_receive(self):
        node = SX126X("/dev/ttyUSB1")
        addr, freq, data = await node.receive()
        self.assertEqual(data, b"Hello")
