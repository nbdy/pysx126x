from unittest import TestCase

from sx126x import BaudRate, Address

from sx126x.enums import TransmitPower, RSSI, TransferMethod, Relay, LBT, WORControl, WORPeriod, AirSpeed, AmbientNoise, \
    PacketSize, Mode, Parity
from sx126x.models import CryptKey
from sx126x.sx126x import SX126X


class HardwareTests(TestCase):
    def setUp(self):
        self.lora = SX126X(
            port="/dev/ttyAMA0",
            write_persist=True,
            mode=Mode.CONFIGURATION,
            debug=True,
            overwrite_defaults=False,
        )

    def tearDown(self):
        del self.lora

    def test_set_mode(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        self.lora.set_mode(Mode.TRANSMISSION)
        self.assertEqual(Mode.TRANSMISSION, self.lora.mode)
        self.lora.set_mode(Mode.WOR)
        self.assertEqual(Mode.WOR, self.lora.mode)
        self.lora.set_mode(Mode.DEEP_SLEEP)
        self.assertEqual(Mode.DEEP_SLEEP, self.lora.mode)

    def test_address_h(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        self.lora.address_h = 69
        self.assertEqual(69, self.lora.address_h)
        self.lora.address_h = 242
        self.assertEqual(242, self.lora.address_h)

    def test_addr_l(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        self.lora.address_l = 42
        self.assertEqual(42, self.lora.address_l)
        self.lora.address_l = 242
        self.assertEqual(242, self.lora.address_l)

    def test_addr(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_address = Address(242, 69)
        self.lora.address = expected_address
        self.assertEqual(expected_address.hi, self.lora.address_h)
        self.assertEqual(expected_address.lo, self.lora.address_l)
        self.assertEqual(expected_address.__str__(), self.lora.address.__str__())
        self.assertEqual(expected_address, self.lora.address)

    def test_net_id(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        self.lora.net_id = 43
        self.assertEqual(43, self.lora.net_id)

    def test_channel(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        for c in range(0, 50):
            self.lora.channel = c
            self.assertEqual(c, self.lora.channel)

    def test_baud_rate(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_baud_rate = BaudRate.B9600
        self.lora.baud_rate = expected_baud_rate
        self.assertEqual(expected_baud_rate, self.lora.baud_rate)

    def test_parity(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_parity = Parity.NONE
        self.lora.parity = expected_parity
        self.assertEqual(expected_parity, self.lora.parity)

    def test_air_speed(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_air_speed = AirSpeed.K4_8
        self.lora.air_speed = expected_air_speed
        self.assertEqual(expected_air_speed, self.lora.air_speed)

    def test_packet_size(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_packet_size = PacketSize.SIZE_128
        self.lora.packet_size = expected_packet_size
        self.assertEqual(expected_packet_size, self.lora.packet_size)

    def test_ambient_noise(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_ambient_noise = AmbientNoise.ENABLED
        self.lora.ambient_noise = expected_ambient_noise
        self.assertEqual(expected_ambient_noise, self.lora.ambient_noise)

    def test_transmit_power(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_transmit_power = TransmitPower.DBM_13
        self.lora.transmit_power = expected_transmit_power
        self.assertEqual(expected_transmit_power, self.lora.transmit_power)

    def test_rssi(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_rssi = RSSI.ENABLED
        self.lora.rssi = expected_rssi
        self.assertEqual(expected_rssi, self.lora.rssi)

    def test_transfer_method(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_transfer_method = TransferMethod.FIXED
        self.lora.transfer_method = expected_transfer_method
        self.assertEqual(expected_transfer_method, self.lora.transfer_method)

    def test_relay(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_relay = Relay.ENABLED
        self.lora.relay = expected_relay
        self.assertEqual(expected_relay, self.lora.relay)

    def test_lbt(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_lbt = LBT.ENABLED
        self.lora.lbt = expected_lbt
        self.assertEqual(expected_lbt, self.lora.lbt)

    def test_wor_control(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_wor_control = WORControl.RECEIVE
        self.lora.wor_control = expected_wor_control
        self.assertEqual(expected_wor_control, self.lora.wor_control)

    def test_wor_period(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_wor_period = WORPeriod.MS_500
        self.lora.wor_period = expected_wor_period
        self.assertEqual(expected_wor_period, self.lora.wor_period)

    def test_crypt_key_h(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        self.lora.crypt_key_h = 222
        self.assertEqual(222, self.lora.crypt_key_h)

    def test_crypt_key_l(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        self.lora.crypt_key_l = 111
        self.assertEqual(111, self.lora.crypt_key_l)

    def test_crypt_key(self):
        self.assertEqual(Mode.CONFIGURATION, self.lora.mode)
        expected_crypt_key = CryptKey(100, 200)
        self.lora.crypt_key = expected_crypt_key
        self.assertEqual(expected_crypt_key.hi, self.lora.crypt_key_h)
        self.assertEqual(expected_crypt_key.lo, self.lora.crypt_key_l)
        self.assertEqual(expected_crypt_key, self.lora.crypt_key)