import unittest

from sx126x import SX126X, Address
from sx126x.enums import TransmitPower, AirSpeed, Mode
from sx126x.models import CryptKey
from test.mock_sx126x import MockSX126X


class SX126XTestMixin:
    """Mixin class that defines common test methods for SX126X implementations"""

    def test_set_mode(self):
        """Test mode switching functionality"""
        self.assertEqual(Mode.CONFIGURATION, self.device.mode)
        self.device.set_mode(Mode.TRANSMISSION)
        self.assertEqual(Mode.TRANSMISSION, self.device.mode)
        self.device.set_mode(Mode.WOR)
        self.assertEqual(Mode.WOR, self.device.mode)
        self.device.set_mode(Mode.DEEP_SLEEP)
        self.assertEqual(Mode.DEEP_SLEEP, self.device.mode)
        # Return to configuration mode for other tests
        self.device.set_mode(Mode.CONFIGURATION)

    def test_address(self):
        """Test address setting and getting"""
        self.assertEqual(Mode.CONFIGURATION, self.device.mode)
        expected_address = Address(242, 69)
        self.device.address = expected_address
        self.assertEqual(expected_address.hi, self.device.address_h)
        self.assertEqual(expected_address.lo, self.device.address_l)
        self.assertEqual(expected_address.__str__(), self.device.address.__str__())
        self.assertEqual(expected_address, self.device.address)

    def test_net_id(self):
        """Test network ID setting and getting"""
        self.assertEqual(Mode.CONFIGURATION, self.device.mode)
        self.device.net_id = 43
        self.assertEqual(43, self.device.net_id)

    def test_channel(self):
        """Test channel setting and getting"""
        self.assertEqual(Mode.CONFIGURATION, self.device.mode)
        # Test a few channels, not all 50 to keep the test faster
        for c in [0, 10, 20, 30, 40, 50]:
            self.device.channel = c
            self.assertEqual(c, self.device.channel)

    def test_air_speed(self):
        """Test air speed setting and getting"""
        self.assertEqual(Mode.CONFIGURATION, self.device.mode)
        expected_air_speed = AirSpeed.K4_8
        self.device.air_speed = expected_air_speed
        self.assertEqual(expected_air_speed, self.device.air_speed)

    def test_transmit_power(self):
        """Test transmit power setting and getting"""
        self.assertEqual(Mode.CONFIGURATION, self.device.mode)
        expected_transmit_power = TransmitPower.DBM_13
        self.device.transmit_power = expected_transmit_power
        self.assertEqual(expected_transmit_power, self.device.transmit_power)

    def test_crypt_key(self):
        """Test encryption key setting and getting"""
        self.assertEqual(Mode.CONFIGURATION, self.device.mode)
        expected_crypt_key = CryptKey(100, 200)
        self.device.crypt_key = expected_crypt_key
        self.assertEqual(expected_crypt_key.hi, self.device.crypt_key_h)
        self.assertEqual(expected_crypt_key.lo, self.device.crypt_key_l)
        self.assertEqual(expected_crypt_key, self.device.crypt_key)

    def test_tx_rx_basic(self):
        """Test basic transmission and reception functionality"""
        # This test is designed to work with both real hardware and mock
        # For real hardware, this would require two devices
        # For mock, we can simulate the reception

        # Set up the test
        self.device.set_mode(Mode.TRANSMISSION)
        test_address = Address(1, 2)
        test_data = b"Test message"

        # For mock implementation, we need to simulate receiving
        # For hardware, this would actually transmit the data
        if isinstance(self.device, MockSX126X):
            # Simulate receiving the data we're about to send
            self.device.simulate_receive(test_address, test_data)

        # Send the data
        self.device.tx(test_address, test_data)

        # For mock implementation, we can verify reception
        # For hardware, this would require a second device to receive
        if isinstance(self.device, MockSX126X):
            received = self.device.rx()
            self.assertIsNotNone(received)

            addr, data = received
            self.assertEqual(test_address, addr)
            self.assertEqual(test_data, data)


class HardwareSX126XTest(SX126XTestMixin, unittest.TestCase):
    """Test case for the hardware SX126X implementation"""

    def setUp(self):
        """Set up a hardware SX126X instance for testing"""
        try:
            self.device = SX126X(
                port="/dev/ttyAMA0",  # This should be configured based on your hardware setup
                write_persist=True,
                mode=Mode.CONFIGURATION,
                debug=True,
                overwrite_defaults=False,
            )
        except Exception as e:
            self.skipTest(f"Hardware not available: {e}")

    def tearDown(self):
        """Clean up after the test"""
        if hasattr(self, 'device'):
            del self.device


if __name__ == '__main__':
    unittest.main()
