from datetime import timedelta
from pathlib import Path
from time import sleep
from typing import Optional, Callable

from loguru import logger
from serial import Serial

from sx126x.enums import AirSpeed, AmbientNoise, BaudRate, Command, Mode, PacketSize, Parity, Register, TransmitPower, \
    RSSI, TransferMethod, Relay, WORControl, WORPeriod, LBT
from sx126x.models import Address, CryptKey
from sx126x.util import get_port


try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    GPIO = None
    logger.warning("RPi.GPIO not imported")


class SX126X(object):
    def __init__(
            self,
            address: Address = Address.parse("242.242"),
            net_id: int = 1,
            channel: int = 1,
            port: Optional[Path | str] = None,
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
        if port is None:
            port = get_port()

        if port is None:
            raise ValueError("Port cannot be None")

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

        if GPIO is not None:
            self.__debug("Setting up GPIO")
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin_m0, GPIO.OUT)
            GPIO.setup(pin_m1, GPIO.OUT)
            self.set_mode(mode)
        else:
            self.__debug("Can't setup GPIO")

        self.serial = Serial(
            port=str(port),
            baudrate=int(baud_rate),
            bytesize=byte_size,
            parity=str(parity),
            stopbits=stop_bits,
            timeout=timeout,
        )

        if overwrite_defaults:
            self.address = address
            self.net_id = net_id
            self.air_speed = air_speed
            self.packet_size = packet_size
            self.ambient_noise = ambient_noise
            self.transmit_power = transmit_power
            self.channel = channel
            self.rssi = rssi
            self.transfer_method = transfer_method
            self.relay = relay
            self.lbt = lbt
            self.wor_control = wor_control
            self.wor_period = wor_period
            self.crypt_key = crypt_key

    def __debug(self, msg: str):
        if self._debug:
            logger.debug(msg)

    def set_mode(self, mode: Mode) -> bool:
        m0_state = None
        m1_state = None

        match mode:
            case Mode.TRANSMISSION:
                m0_state = 0
                m1_state = 0
            case Mode.CONFIGURATION:
                m0_state = 0
                m1_state = 1
            case Mode.WOR:
                m0_state = 1
                m1_state = 0
            case Mode.DEEP_SLEEP:
                m0_state = 1
                m1_state = 1

        if m0_state is not None and m1_state is not None:
            if GPIO is not None:
                self.__debug(f"Switching to mode: {mode}")
                GPIO.output(self._pin_m0, m0_state)
                GPIO.output(self._pin_m1, m1_state)
            self._mode = mode
            return True
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def _write(
            self,
            data: bytes,
            retries: int = 3,
            retry_delay: timedelta = timedelta(seconds=1),
            read_length: Optional[int] = None,
    ) -> Optional[bytes]:
        self.serial.flush()
        self.serial.write(data)
        data_len = len(data)
        rcv = self.serial.read(data_len + read_length if read_length is not None else data_len)
        if len(rcv) == 0:
            logger.warning("Could not write command. Trying again.")
            if retries > 0:
                retries -= 1
                sleep(retry_delay.total_seconds())
                return self._write(data, retries, retry_delay)
            else:
                logger.error("No retries left. Operation failed.")
                return None
        self.__debug(f"TX: {data}")
        self.__debug(f"RX: {rcv}")
        return rcv[data_len:]

    def _read_cmd(
            self,
            reg: Register,
            size: int = 1,
            retries: int = 3,
            retry_delay: timedelta = timedelta(seconds=1)
    ) -> Optional[bytes]:
        return self._write(
            bytes([Command.READ, reg, size]), retries, retry_delay, size
        )

    def _write_cmd(
            self,
            reg: Register,
            data: bytes | int,
            retries: int = 3,
            retry_delay: timedelta = timedelta(seconds=1),
            cmd: Command = Command.WRITE,
    ) -> bool:
        if isinstance(data, int):
            data = data.to_bytes()
        if not self._write_persist and cmd == Command.WRITE:
            cmd = Command.WRITE_TEMP
        d2s = bytes([cmd, reg, len(data)]) + data
        rcv = self._write(d2s, retries, retry_delay)
        if rcv:
            return rcv[1:] == d2s[1:]
        else:
            return False

    @property
    def mode(self) -> Mode:
        return self._mode

    @mode.setter
    def mode(self, mode: Mode):
        self.set_mode(mode)

    @property
    def address_h(self) -> int:
        if self._mode == Mode.CONFIGURATION:
            self._address.hi = int.from_bytes(self._read_cmd(Register.ADDR_HIGH))
        return self._address.hi

    @address_h.setter
    def address_h(self, value: int):
        self._address.hi = value
        if self._mode == Mode.CONFIGURATION:
            self._write_cmd(Register.ADDR_HIGH, value)

    @property
    def address_l(self) -> int:
        if self._mode == Mode.CONFIGURATION:
            self._address.lo = int.from_bytes(self._read_cmd(Register.ADDR_LOW))
        return self._address.lo

    @address_l.setter
    def address_l(self, value: int):
        self._address.lo = value
        if self._mode == Mode.CONFIGURATION:
            self._write_cmd(Register.ADDR_LOW, value)

    @property
    def address(self) -> Address:
        return self._address

    @address.setter
    def address(self, value: Address):
        if self._mode == Mode.CONFIGURATION:
            self._write_cmd(Register.ADDR_HIGH, value.to_bytes())
        self._address = value

    @property
    def net_id(self) -> int:
        if self._mode == Mode.CONFIGURATION:
            self._net_id = int.from_bytes(self._read_cmd(Register.NET_ID))
        return self._net_id

    @net_id.setter
    def net_id(self, value: int):
        self._net_id = value
        if self._mode == Mode.CONFIGURATION:
            self._write_cmd(Register.NET_ID, value)

    @property
    def baud_rate(self) -> BaudRate:
        if self._mode == Mode.CONFIGURATION:
            self._baud_rate = BaudRate.from_data(int.from_bytes(self._read_cmd(Register.COMMUNICATION)))
        return self._baud_rate

    @baud_rate.setter
    def baud_rate(self, value: BaudRate):
        # TODO: Reopen serial port
        if self._mode == Mode.CONFIGURATION:
            communication_data = int.from_bytes(self._read_cmd(Register.COMMUNICATION))
            self._write_cmd(Register.COMMUNICATION, value.apply_to(communication_data))
        self._baud_rate = value

    @property
    def parity(self) -> Parity:
        if self._mode == Mode.CONFIGURATION:
            self._parity = Parity.from_data(int.from_bytes(self._read_cmd(Register.COMMUNICATION)))
        return self._parity

    @parity.setter
    def parity(self, value: Parity):
        # TODO: Reopen serial port
        if self._mode == Mode.CONFIGURATION:
            communication_data = int.from_bytes(self._read_cmd(Register.COMMUNICATION))
            self._write_cmd(Register.COMMUNICATION, value.apply_to(communication_data))
        self._parity = value

    @property
    def air_speed(self) -> AirSpeed:
        if self._mode == Mode.CONFIGURATION:
            self._air_speed = AirSpeed.from_data(int.from_bytes(self._read_cmd(Register.COMMUNICATION)))
        return self._air_speed

    @air_speed.setter
    def air_speed(self, value: AirSpeed):
        if self._mode == Mode.CONFIGURATION:
            communication_data = int.from_bytes(self._read_cmd(Register.COMMUNICATION))
            self._write_cmd(Register.COMMUNICATION, value.apply_to(communication_data))
        self._air_speed = value

    @property
    def packet_size(self) -> PacketSize:
        if self._mode == Mode.CONFIGURATION:
            self._packet_size = PacketSize.from_data(int.from_bytes(self._read_cmd(Register.COMMUNICATION)))
        return self._packet_size

    @packet_size.setter
    def packet_size(self, value: PacketSize):
        if self._mode == Mode.CONFIGURATION:
            transmission_data = int.from_bytes(self._read_cmd(Register.TRANSMISSION))
            self._write_cmd(Register.TRANSMISSION, value.apply_to(transmission_data), cmd=Command.WIRELESS_CFG)
        self._packet_size = value

    @property
    def ambient_noise(self) -> AmbientNoise:
        if self._mode == Mode.CONFIGURATION:
            self._ambient_noise = AmbientNoise.from_data(int.from_bytes(self._read_cmd(Register.TRANSMISSION)))
        return self._ambient_noise

    @ambient_noise.setter
    def ambient_noise(self, value: AmbientNoise):
        if self._mode == Mode.CONFIGURATION:
            transmission_data = int.from_bytes(self._read_cmd(Register.TRANSMISSION))
            self._write_cmd(Register.TRANSMISSION, value.apply_to(transmission_data))
        self._ambient_noise = value

    @property
    def transmit_power(self) -> TransmitPower:
        if self._mode == Mode.CONFIGURATION:
            self._transmit_power = TransmitPower.from_data(int.from_bytes(self._read_cmd(Register.TRANSMISSION)))
        return self._transmit_power

    @transmit_power.setter
    def transmit_power(self, value: TransmitPower):
        if self._mode == Mode.CONFIGURATION:
            transmission_data = int.from_bytes(self._read_cmd(Register.TRANSMISSION))
            self._write_cmd(Register.TRANSMISSION, value.apply_to(transmission_data))
        self._transmit_power = value

    @property
    def channel(self) -> int:
        if self._mode == Mode.CONFIGURATION:
            self._channel = int.from_bytes(self._read_cmd(Register.CHANNEL))
        return self._channel

    @channel.setter
    def channel(self, value: int):
        if value < 0 or value > 83:
            raise ValueError("Channel must be in range (0, 83)")
        self._channel = value
        if self._mode == Mode.CONFIGURATION:
            self._write_cmd(Register.CHANNEL, value)

    @property
    def rssi(self) -> RSSI:
        if self._mode == Mode.CONFIGURATION:
            self._rssi = RSSI.from_data(int.from_bytes(self._read_cmd(Register.MODE)))
        return self._rssi

    @rssi.setter
    def rssi(self, value: RSSI):
        if self._mode == Mode.CONFIGURATION:
            mode_data = int.from_bytes(self._read_cmd(Register.MODE))
            self._write_cmd(Register.MODE, value.apply_to(mode_data))
        self._rssi = value

    @property
    def transfer_method(self) -> TransferMethod:
        if self._mode == Mode.CONFIGURATION:
            self._transfer_method = TransferMethod.from_data(int.from_bytes(self._read_cmd(Register.MODE)))
        return self._transfer_method

    @transfer_method.setter
    def transfer_method(self, value: TransferMethod):
        if self._mode == Mode.CONFIGURATION:
            mode_data = int.from_bytes(self._read_cmd(Register.MODE))
            self._write_cmd(Register.MODE, value.apply_to(mode_data))
        self._transfer_method = value

    @property
    def relay(self) -> Relay:
        if self._mode == Mode.CONFIGURATION:
            self._relay = Relay.from_data(int.from_bytes(self._read_cmd(Register.MODE)))
        return self._relay

    @relay.setter
    def relay(self, value: Relay):
        if self._mode == Mode.CONFIGURATION:
            mode_data = int.from_bytes(self._read_cmd(Register.MODE))
            self._write_cmd(Register.MODE, value.apply_to(mode_data))
        self._relay = value

    @property
    def lbt(self) -> LBT:
        if self._mode == Mode.CONFIGURATION:
            self._lbt = LBT.from_data(int.from_bytes(self._read_cmd(Register.MODE)))
        return self._lbt

    @lbt.setter
    def lbt(self, value: LBT):
        if self._mode == Mode.CONFIGURATION:
            mode_data = int.from_bytes(self._read_cmd(Register.MODE))
            self._write_cmd(Register.MODE, value.apply_to(mode_data))
        self._lbt = value

    @property
    def wor_control(self) -> WORControl:
        if self._mode == Mode.CONFIGURATION:
            self._wor_control = WORControl.from_data(int.from_bytes(self._read_cmd(Register.MODE)))
        return self._wor_control

    @wor_control.setter
    def wor_control(self, value: WORControl):
        if self._mode == Mode.CONFIGURATION:
            mode_data = int.from_bytes(self._read_cmd(Register.MODE))
            self._write_cmd(Register.MODE, value.apply_to(mode_data))
        self._wor_control = value

    @property
    def wor_period(self) -> WORPeriod:
        if self._mode == Mode.CONFIGURATION:
            self._wor_period = WORPeriod.from_data(int.from_bytes(self._read_cmd(Register.MODE)))
        return self._wor_period

    @wor_period.setter
    def wor_period(self, value: WORPeriod):
        if self._mode == Mode.CONFIGURATION:
            mode_data = int.from_bytes(self._read_cmd(Register.MODE))
            self._write_cmd(Register.MODE, value.apply_to(mode_data))
        self._wor_period = value

    @property
    def crypt_key_h(self) -> int:
        if self._mode == Mode.CONFIGURATION:
            self._crypt_key.hi = int.from_bytes(self._read_cmd(Register.CRYPT_HIGH))
        return self._crypt_key.hi

    @crypt_key_h.setter
    def crypt_key_h(self, value: int):
        if self._mode == Mode.CONFIGURATION:
            self._write_cmd(Register.CRYPT_HIGH, value)
        self._crypt_key.hi = value

    @property
    def crypt_key_l(self) -> int:
        if self._mode == Mode.CONFIGURATION:
            self._crypt_key.lo = int.from_bytes(self._read_cmd(Register.CRYPT_LOW))
        return self._crypt_key.lo

    @crypt_key_l.setter
    def crypt_key_l(self, value: int):
        if self._mode == Mode.CONFIGURATION:
            self._write_cmd(Register.CRYPT_LOW, value)
        self._crypt_key.lo = value

    @property
    def crypt_key(self) -> CryptKey:
        return CryptKey(self.crypt_key_h, self.crypt_key_l)

    @crypt_key.setter
    def crypt_key(self, value: CryptKey):
        if self._mode == Mode.CONFIGURATION:
            self._write_cmd(Register.CRYPT_HIGH, value.to_bytes())
        self._crypt_key = value

    def tx(self, address: Address, data: bytes):
        if self._transfer_method == TransferMethod.FIXED:
            d2s = bytes([
                address.hi,
                address.lo,
                self.channel,
                self.address_h,
                self.address_l,
            ]) + data
        else:
            d2s = data
        self.serial.write(d2s)
        self.serial.flush()

    def rx(self, size: Optional[int] = None) -> Optional[tuple[Address, bytes]]:
        data = self.serial.read(self.serial.in_waiting if size is None else size)
        if len(data) == 0:
            return None
        if len(data) < 6:
            logger.debug(f"Received data: {data}")
            return None
        tx_addr = Address(data[0], data[1])
        payload = data[2:]
        return tx_addr, payload

    def rx_loop(self, cb: Callable[[Address, bytes], bool]):
        """
        Run rx in a loop and call cb function with data.
        If cb function returns False we exit
        :param cb:
        :return:
        """
        do_run = True
        while do_run:
            args = self.rx()
            if args is None:
                sleep(0.1)
            else:
                do_run = cb(*args)

    def to_json(self):
        cls = self.__class__
        return {
            name: getattr(self, name)
            for name in dir(cls)
            if isinstance(getattr(cls, name), property)
        }
