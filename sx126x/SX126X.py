from serial import Serial


class SX126X(object):
    start_frequency: int = 850
    offset_frequency: int = 18

    def __init__(self, port: str, frequency: int = 868, address: int = 0x00, power: int = 22, rssi: bool = True):
        self.port = port
        self.frequency = frequency
        self.address = address
        self.power = power
        self.rssi = rssi

        self.serial = Serial(port, 9600)
        self.serial.flushInput()

    def __del__(self):
        self.serial.close()

    async def send(self, data: bytes):
        print("Sending:", data)
        self.serial.write(data)

    async def send_to(self, rx_addr: int, frequency: int, payload: bytes):
        offset_frequency = frequency - (850 if frequency > 850 else 410)
        data = \
            bytes([rx_addr >> 8]) + \
            bytes([rx_addr & 0xff]) + \
            bytes([offset_frequency]) + \
            bytes([self.address >> 8]) + \
            bytes([self.address & 0xff]) + \
            bytes([self.offset_frequency]) + \
            payload
        await self.send(data)

    async def receive(self) -> (int, int, int, bytes):
        """
        :return: (tx, rx, freq, payload)
        """
        size = self.serial.inWaiting()
        if size > 0:
            buf = self.serial.read(size)
            tx_addr = (buf[0] << 8) + buf[1]
            frequency = buf[2] + self.start_frequency
            rx_addr = (buf[3] << 8) + buf[4]
            payload = buf[6:-1]
            return tx_addr, rx_addr, frequency, payload
        return None, None, None, None
