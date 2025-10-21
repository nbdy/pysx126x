from time import sleep
from typing import Optional, Callable, Dict, Any

from loguru import logger

from sx126x.enums import AirSpeed, AmbientNoise, BaudRate, Mode, PacketSize, Parity, Register, TransmitPower, \
    RSSI, TransferMethod, Relay, WORControl, WORPeriod, LBT
from sx126x.models import Address, CryptKey


class MockSX126X:
    """
    A mock implementation of the SX126X class that simulates the bit-encoded properties
    of the SX1262 without requiring the actual hardware.
    """
    def __init__(
            self,
            address: Address = Address.parse("242.242"),
            net_id: int = 1,
            channel: int = 1,
            port: Optional[str] = None,
            pin_m0: int = 6,
            pin_m1: int = 5,
            baud_rate: BaudRate = BaudRate.B9600,
            byte_size: int = 8,
            parity: Parity = Parity.NONE,
            stop_bits: int = 1,
            write_persist: bool = False,
            mode: Mode = Mode.CONFIGURATION,
            timeout: float = 2,
            debug: bool = False,
            air_speed: AirSpeed = AirSpeed.K2_4,
            packet_size: PacketSize = PacketSize.SIZE_128,
            ambient_noise: AmbientNoise = AmbientNoise.DISABLED,
            transmit_power: TransmitPower = TransmitPower.DBM_22,
            rssi: RSSI = RSSI.DISABLED,
            transfer_method: TransferMethod = TransferMethod.FIXED,
            relay: Relay = Relay.DISABLED,
            lbt: LBT = LBT.DISABLED,
            wor_control: WORControl = WORControl.TRANSMIT,
            wor_period: WORPeriod = WORPeriod.MS_500,
            crypt_key: CryptKey = CryptKey(0, 0),
            overwrite_defaults: bool = True
    ):
        self._address = address
        self._net_id = net_id
        self._channel = channel
        self._port = port
        self._baud_rate = baud_rate
        self._byte_size = byte_size
        self._parity = parity
        self._stop_bits = stop_bits
        self._pin_m0 = pin_m0
        self._pin_m1 = pin_m1
        self._write_persist = write_persist
        self._debug = debug
        self._mode = mode
        self._air_speed = air_speed
        self._packet_size = packet_size
        self._ambient_noise = ambient_noise
        self._transmit_power = transmit_power
        self._rssi = rssi
        self._transfer_method = transfer_method
        self._relay = relay
        self._lbt = lbt
        self._wor_control = wor_control
        self._wor_period = wor_period
        self._crypt_key = crypt_key
        
        # Simulated registers
        self._registers: Dict[Register, int] = {
            Register.ADDR_HIGH: address.hi,
            Register.ADDR_LOW: address.lo,
            Register.NET_ID: net_id,
            Register.CHANNEL: channel,
            Register.CRYPT_HIGH: crypt_key.hi,
            Register.CRYPT_LOW: crypt_key.lo,
        }
        
        # Initialize communication register
        comm_reg = 0
        comm_reg = air_speed.apply_to(comm_reg)
        comm_reg = baud_rate.apply_to(comm_reg)
        comm_reg = parity.apply_to(comm_reg)
        self._registers[Register.COMMUNICATION] = comm_reg
        
        # Initialize transmission register
        trans_reg = 0
        trans_reg = packet_size.apply_to(trans_reg)
        trans_reg = ambient_noise.apply_to(trans_reg)
        trans_reg = transmit_power.apply_to(trans_reg)
        self._registers[Register.TRANSMISSION] = trans_reg
        
        # Initialize mode register
        mode_reg = 0
        mode_reg = rssi.apply_to(mode_reg)
        mode_reg = transfer_method.apply_to(mode_reg)
        mode_reg = relay.apply_to(mode_reg)
        mode_reg = lbt.apply_to(mode_reg)
        mode_reg = wor_control.apply_to(mode_reg)
        mode_reg = wor_period.apply_to(mode_reg)
        self._registers[Register.MODE] = mode_reg
        
        # Simulated received data queue
        self._rx_queue = []

    def __debug(self, msg: str):
        if self._debug:
            logger.debug(msg)

    def set_mode(self, mode: Mode) -> bool:
        self.__debug(f"Switching to mode: {mode}")
        self._mode = mode
        return True

    def _read_register(self, reg: Register) -> int:
        return self._registers.get(reg, 0)

    def _write_register(self, reg: Register, value: int) -> bool:
        self._registers[reg] = value
        return True

    @property
    def mode(self) -> Mode:
        return self._mode

    @mode.setter
    def mode(self, mode: Mode):
        self.set_mode(mode)

    @property
    def address_h(self) -> int:
        if self._mode == Mode.CONFIGURATION:
            self._address.hi = self._read_register(Register.ADDR_HIGH)
        return self._address.hi

    @address_h.setter
    def address_h(self, value: int):
        self._address.hi = value
        if self._mode == Mode.CONFIGURATION:
            self._write_register(Register.ADDR_HIGH, value)

    @property
    def address_l(self) -> int:
        if self._mode == Mode.CONFIGURATION:
            self._address.lo = self._read_register(Register.ADDR_LOW)
        return self._address.lo

    @address_l.setter
    def address_l(self, value: int):
        self._address.lo = value
        if self._mode == Mode.CONFIGURATION:
            self._write_register(Register.ADDR_LOW, value)

    @property
    def address(self) -> Address:
        return self._address

    @address.setter
    def address(self, value: Address):
        if self._mode == Mode.CONFIGURATION:
            self._write_register(Register.ADDR_HIGH, value.hi)
            self._write_register(Register.ADDR_LOW, value.lo)
        self._address = value

    @property
    def net_id(self) -> int:
        if self._mode == Mode.CONFIGURATION:
            self._net_id = self._read_register(Register.NET_ID)
        return self._net_id

    @net_id.setter
    def net_id(self, value: int):
        self._net_id = value
        if self._mode == Mode.CONFIGURATION:
            self._write_register(Register.NET_ID, value)

    @property
    def baud_rate(self) -> BaudRate:
        if self._mode == Mode.CONFIGURATION:
            self._baud_rate = BaudRate.from_data(self._read_register(Register.COMMUNICATION))
        return self._baud_rate

    @baud_rate.setter
    def baud_rate(self, value: BaudRate):
        if self._mode == Mode.CONFIGURATION:
            comm_data = self._read_register(Register.COMMUNICATION)
            self._write_register(Register.COMMUNICATION, value.apply_to(comm_data))
        self._baud_rate = value

    @property
    def parity(self) -> Parity:
        if self._mode == Mode.CONFIGURATION:
            self._parity = Parity.from_data(self._read_register(Register.COMMUNICATION))
        return self._parity

    @parity.setter
    def parity(self, value: Parity):
        if self._mode == Mode.CONFIGURATION:
            comm_data = self._read_register(Register.COMMUNICATION)
            self._write_register(Register.COMMUNICATION, value.apply_to(comm_data))
        self._parity = value

    @property
    def air_speed(self) -> AirSpeed:
        if self._mode == Mode.CONFIGURATION:
            self._air_speed = AirSpeed.from_data(self._read_register(Register.COMMUNICATION))
        return self._air_speed

    @air_speed.setter
    def air_speed(self, value: AirSpeed):
        if self._mode == Mode.CONFIGURATION:
            comm_data = self._read_register(Register.COMMUNICATION)
            self._write_register(Register.COMMUNICATION, value.apply_to(comm_data))
        self._air_speed = value

    @property
    def packet_size(self) -> PacketSize:
        if self._mode == Mode.CONFIGURATION:
            self._packet_size = PacketSize.from_data(self._read_register(Register.TRANSMISSION))
        return self._packet_size

    @packet_size.setter
    def packet_size(self, value: PacketSize):
        if self._mode == Mode.CONFIGURATION:
            trans_data = self._read_register(Register.TRANSMISSION)
            self._write_register(Register.TRANSMISSION, value.apply_to(trans_data))
        self._packet_size = value

    @property
    def ambient_noise(self) -> AmbientNoise:
        if self._mode == Mode.CONFIGURATION:
            self._ambient_noise = AmbientNoise.from_data(self._read_register(Register.TRANSMISSION))
        return self._ambient_noise

    @ambient_noise.setter
    def ambient_noise(self, value: AmbientNoise):
        if self._mode == Mode.CONFIGURATION:
            trans_data = self._read_register(Register.TRANSMISSION)
            self._write_register(Register.TRANSMISSION, value.apply_to(trans_data))
        self._ambient_noise = value

    @property
    def transmit_power(self) -> TransmitPower:
        if self._mode == Mode.CONFIGURATION:
            self._transmit_power = TransmitPower.from_data(self._read_register(Register.TRANSMISSION))
        return self._transmit_power

    @transmit_power.setter
    def transmit_power(self, value: TransmitPower):
        if self._mode == Mode.CONFIGURATION:
            trans_data = self._read_register(Register.TRANSMISSION)
            self._write_register(Register.TRANSMISSION, value.apply_to(trans_data))
        self._transmit_power = value

    @property
    def channel(self) -> int:
        if self._mode == Mode.CONFIGURATION:
            self._channel = self._read_register(Register.CHANNEL)
        return self._channel

    @channel.setter
    def channel(self, value: int):
        if value < 0 or value > 83:
            raise ValueError("Channel must be in range (0, 83)")
        self._channel = value
        if self._mode == Mode.CONFIGURATION:
            self._write_register(Register.CHANNEL, value)

    @property
    def rssi(self) -> RSSI:
        if self._mode == Mode.CONFIGURATION:
            self._rssi = RSSI.from_data(self._read_register(Register.MODE))
        return self._rssi

    @rssi.setter
    def rssi(self, value: RSSI):
        if self._mode == Mode.CONFIGURATION:
            mode_data = self._read_register(Register.MODE)
            self._write_register(Register.MODE, value.apply_to(mode_data))
        self._rssi = value

    @property
    def transfer_method(self) -> TransferMethod:
        if self._mode == Mode.CONFIGURATION:
            self._transfer_method = TransferMethod.from_data(self._read_register(Register.MODE))
        return self._transfer_method

    @transfer_method.setter
    def transfer_method(self, value: TransferMethod):
        if self._mode == Mode.CONFIGURATION:
            mode_data = self._read_register(Register.MODE)
            self._write_register(Register.MODE, value.apply_to(mode_data))
        self._transfer_method = value

    @property
    def relay(self) -> Relay:
        if self._mode == Mode.CONFIGURATION:
            self._relay = Relay.from_data(self._read_register(Register.MODE))
        return self._relay

    @relay.setter
    def relay(self, value: Relay):
        if self._mode == Mode.CONFIGURATION:
            mode_data = self._read_register(Register.MODE)
            self._write_register(Register.MODE, value.apply_to(mode_data))
        self._relay = value

    @property
    def lbt(self) -> LBT:
        if self._mode == Mode.CONFIGURATION:
            self._lbt = LBT.from_data(self._read_register(Register.MODE))
        return self._lbt

    @lbt.setter
    def lbt(self, value: LBT):
        if self._mode == Mode.CONFIGURATION:
            mode_data = self._read_register(Register.MODE)
            self._write_register(Register.MODE, value.apply_to(mode_data))
        self._lbt = value

    @property
    def wor_control(self) -> WORControl:
        if self._mode == Mode.CONFIGURATION:
            self._wor_control = WORControl.from_data(self._read_register(Register.MODE))
        return self._wor_control

    @wor_control.setter
    def wor_control(self, value: WORControl):
        if self._mode == Mode.CONFIGURATION:
            mode_data = self._read_register(Register.MODE)
            self._write_register(Register.MODE, value.apply_to(mode_data))
        self._wor_control = value

    @property
    def wor_period(self) -> WORPeriod:
        if self._mode == Mode.CONFIGURATION:
            self._wor_period = WORPeriod.from_data(self._read_register(Register.MODE))
        return self._wor_period

    @wor_period.setter
    def wor_period(self, value: WORPeriod):
        if self._mode == Mode.CONFIGURATION:
            mode_data = self._read_register(Register.MODE)
            self._write_register(Register.MODE, value.apply_to(mode_data))
        self._wor_period = value

    @property
    def crypt_key_h(self) -> int:
        if self._mode == Mode.CONFIGURATION:
            self._crypt_key.hi = self._read_register(Register.CRYPT_HIGH)
        return self._crypt_key.hi

    @crypt_key_h.setter
    def crypt_key_h(self, value: int):
        if self._mode == Mode.CONFIGURATION:
            self._write_register(Register.CRYPT_HIGH, value)
        self._crypt_key.hi = value

    @property
    def crypt_key_l(self) -> int:
        if self._mode == Mode.CONFIGURATION:
            self._crypt_key.lo = self._read_register(Register.CRYPT_LOW)
        return self._crypt_key.lo

    @crypt_key_l.setter
    def crypt_key_l(self, value: int):
        if self._mode == Mode.CONFIGURATION:
            self._write_register(Register.CRYPT_LOW, value)
        self._crypt_key.lo = value

    @property
    def crypt_key(self) -> CryptKey:
        return CryptKey(self.crypt_key_h, self.crypt_key_l)

    @crypt_key.setter
    def crypt_key(self, value: CryptKey):
        if self._mode == Mode.CONFIGURATION:
            self._write_register(Register.CRYPT_HIGH, value.hi)
            self._write_register(Register.CRYPT_LOW, value.lo)
        self._crypt_key = value

    def tx(self, address: Address, data: bytes):
        """
        Simulate transmitting data to the specified address.
        In a real implementation, this would be received by another SX126X instance.
        """
        self.__debug(f"TX: {address} {data}")
        # In a real implementation, this would send data over the air
        # For testing, you could add a callback or event system to notify other mock instances

    def rx(self, size: Optional[int] = None) -> Optional[tuple[Address, bytes]]:
        """
        Simulate receiving data.
        In a real implementation, this would receive data from another SX126X instance.
        """
        if not self._rx_queue:
            return None
        
        addr, data = self._rx_queue.pop(0)
        self.__debug(f"RX: {addr} {data}")
        return addr, data

    def rx_loop(self, cb: Callable[[Address, bytes], bool]):
        """
        Run rx in a loop and call cb function with data.
        If cb function returns False we exit
        """
        do_run = True
        while do_run:
            args = self.rx()
            if args is None:
                sleep(0.1)
            else:
                do_run = cb(*args)

    def to_json(self) -> Dict[str, Any]:
        """
        Return a JSON-serializable dictionary of the current configuration.
        """
        return {
            "address": str(self._address),
            "net_id": self._net_id,
            "channel": self._channel,
            "baud_rate": str(self._baud_rate),
            "parity": str(self._parity),
            "air_speed": str(self._air_speed),
            "packet_size": str(self._packet_size),
            "ambient_noise": str(self._ambient_noise),
            "transmit_power": str(self._transmit_power),
            "rssi": str(self._rssi),
            "transfer_method": str(self._transfer_method),
            "relay": str(self._relay),
            "lbt": str(self._lbt),
            "wor_control": str(self._wor_control),
            "wor_period": str(self._wor_period),
            "crypt_key": str(self._crypt_key),
            "mode": str(self._mode)
        }
    
    # Methods for testing/simulation
    
    def simulate_receive(self, address: Address, data: bytes):
        """
        Simulate receiving data from the specified address.
        This is used for testing to inject data into the rx queue.
        """
        self._rx_queue.append((address, data))