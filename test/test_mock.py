import unittest

from sx126x import Address
from sx126x.enums import Mode
from test.mock_sx126x import MockSX126X
from test.test_common import SX126XTestMixin


class MockSX126XTest(SX126XTestMixin, unittest.TestCase):
    """Test case for the MockSX126X implementation"""

    def setUp(self):
        """Set up a MockSX126X instance for testing"""
        self.device = MockSX126X(
            write_persist=True,
            mode=Mode.CONFIGURATION,
            debug=True,
            overwrite_defaults=False,
        )

    def tearDown(self):
        """Clean up after the test"""
        del self.device

    def test_simulate_receive(self):
        """Test the simulate_receive functionality specific to MockSX126X"""
        self.device.set_mode(Mode.TRANSMISSION)
        test_address = Address(1, 2)
        test_data = b"Test message"

        # Initially, there should be no data to receive
        self.assertIsNone(self.device.rx())

        # Simulate receiving data
        self.device.simulate_receive(test_address, test_data)

        # Now we should be able to receive the data
        received = self.device.rx()
        self.assertIsNotNone(received)

        addr, data = received
        self.assertEqual(test_address, addr)
        self.assertEqual(test_data, data)


if __name__ == '__main__':
    unittest.main()
