# SX126X Project Development Guidelines

This document provides guidelines and information for developers working on the SX126X project.

## Build/Configuration Instructions

### Installation

The SX126X library can be installed using pip:

```shell
pip install sx126x
```

### Development Setup

For development, it's recommended to install the package in development mode:

```shell
# Clone the repository
git clone https://github.com/nbdy/pysx126x.git
cd pysx126x

# Install in development mode
pip install -e .
```

### Dependencies

The project has the following dependencies:
- Python >= 3.8
- pyserial == 3.5
- RPi.GPIO == 0.7.1 (only required when running on Raspberry Pi)

## Testing Information

### Running Tests

The project uses Python's built-in unittest framework for testing. Tests are located in the `test` directory.

To run all tests:

```shell
python -m unittest discover test
```

To run a specific test file:

```shell
python test/configuration.py
```

### Hardware Tests

Many tests in the `test/configuration.py` file require physical SX126X hardware connected to a Raspberry Pi. These tests are designed to verify that the library can correctly configure and communicate with the hardware.

When running hardware tests, ensure:
1. The SX126X module is properly connected to the Raspberry Pi
2. The correct serial port is specified (default is `/dev/ttyAMA0`)
3. The correct GPIO pins are specified for M0 and M1 (defaults are 6 and 5)

### Mock Tests

For development without hardware, you can use mock tests that simulate the hardware. An example mock test is provided in `test/mock_test.py`.

To run the mock test:

```shell
python test/mock_test.py
```

This test demonstrates how to use unittest.mock to mock the serial port and GPIO dependencies, allowing tests to run in any environment.

### Creating New Tests

When creating new tests:

1. Create a new test file in the `test` directory
2. Import the necessary modules and classes
3. Create a test class that inherits from `unittest.TestCase`
4. Implement test methods that start with `test_`
5. Use assertions to verify expected behavior

Hardware independent tests should not be done.
All testing should happen on the Raspberry Pi with the IP 10.0.0.203 and the username 'nbdy'.

## Additional Development Information

### Code Style

The project follows standard Python coding conventions:
- Use 4 spaces for indentation
- Follow PEP 8 guidelines for naming and style
- Use type hints for function parameters and return values

### Project Structure

- `sx126x/`: Main package directory
  - `__init__.py`: Package initialization
  - `sx126x.py`: Main SX126X class implementation
  - `util.py`: Utility functions
  - `enums/`: Enumeration classes for various settings
  - `models/`: Data model classes (Address, CryptKey)
- `example/`: Example scripts demonstrating usage
  - `defaults.py`: Shows default configuration
  - `rx.py`: Example receiver implementation
  - `tx.py`: Example transmitter implementation
- `test/`: Test files

### Key Classes and Methods

- `SX126X`: Main class for interacting with SX126X modules
  - `__init__`: Initializes the module with specified parameters
  - `set_mode`: Sets the operating mode (CONFIGURATION, TRANSMISSION, WOR, DEEP_SLEEP)
  - `tx`: Transmits data to a specified address
  - `rx`: Receives data
  - `rx_loop`: Continuously receives data and calls a callback function

### Configuration Parameters

The SX126X class accepts numerous configuration parameters, all documented in the README.md file. Key parameters include:
- `address`: Device address (default: Address.parse("242.242"))
- `net_id`: Network ID (default: 1)
- `channel`: Channel (default: 1)
- `port`: Serial port path (default: None, auto-detected)
- `pin_m0`/`pin_m1`: GPIO pins for mode selection (defaults: 6, 5)
- `mode`: Operating mode (default: Mode.CONFIGURATION)

### Debugging

To enable debug logging, set the `debug` parameter to `True` when initializing the SX126X class:

```python
lora = SX126X(debug=True)
```

This will print detailed information about commands sent to and received from the device.

### Common Issues

1. **Serial Port Access**: Ensure the user has permission to access the serial port. On Linux, add the user to the `dialout` group:
   ```shell
   sudo usermod -a -G dialout $USER
   ```

2. **GPIO Access**: On Raspberry Pi, GPIO access requires root privileges or membership in the `gpio` group.

3. **Hardware Connectivity**: Verify that the SX126X module is properly connected and that the correct pins are specified for M0 and M1.

4. **Persistence Issues**: When testing configuration changes, set `write_persist=True` to make changes persistent across power cycles.

### External Information

Information about the module can be found here: https://www.waveshare.com/wiki/SX1262_868M_LoRa_HAT

Information about the registers is here: https://www.waveshare.com/wiki/LoRa-HAT-Reg

Information about the serial protocol is here: https://www.waveshare.com/wiki/LoRa-HAT-Control
