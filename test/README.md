# SX126X Test Suite

This directory contains tests for the SX126X library, including tests for both the hardware implementation and the mock implementation.

## Test Structure

The test suite is organized as follows:

- `test_hardware.py`: Tests for the hardware SX126X configuration settings
- `test_common.py`: Contains a mixin class that defines common test methods and the hardware test class
- `test_mock.py`: Tests for the mock implementation

The `test_common.py` file contains a mixin class (`SX126XTestMixin`) that defines common test methods, and the hardware test class:

- `HardwareSX126XTest`: Tests for the hardware implementation

The `test_mock.py` file contains:

- `MockSX126XTest`: Tests for the mock implementation

## Dependencies

The tests require the following Python packages:

- `loguru`: Used for logging
- `pyserial`: Used for serial communication (for hardware tests)

You can install these dependencies with pip:

```bash
pip install loguru pyserial
```

## Running the Tests

### Running All Tests

To run all tests, use the following command:

```bash
python -m unittest discover -s test
```

### Running Specific Tests

To run only the mock tests (which don't require hardware):

```bash
python -m unittest test.test_mock
```

To run the hardware tests (requires connected hardware):

```bash
python -m unittest test.test_hardware
```

To run only the common hardware test class (also requires connected hardware):

```bash
python -m unittest test.test_common.HardwareSX126XTest
```

## Hardware Configuration

The hardware tests are configured to use `/dev/ttyAMA0` as the serial port. If your hardware is connected to a different port, you'll need to modify the `setUp` method in the `HardwareSX126XTest` class.

If the hardware is not available, the tests will be skipped with an appropriate message.

## Mock Testing

The mock tests use the `MockSX126X` class to simulate the behavior of the SX126X hardware. This allows testing the library's functionality without requiring the actual hardware.

The mock implementation includes a `simulate_receive` method that can be used to inject data into the receive queue, simulating data being received over the air.

## CI/CD Pipeline Testing

In our continuous integration pipeline, we run mock tests for our mocked hardware for several important reasons:

1. **Hardware Independence**: The mock tests allow us to verify the library's functionality without requiring physical SX126X hardware, making the tests runnable in any CI environment.

2. **Consistent Testing Environment**: Using mocks ensures that tests run in a consistent, controlled environment, eliminating variables like hardware differences or connection issues.

3. **Faster Feedback**: Mock tests run much faster than hardware tests, providing quicker feedback on code changes.

4. **Comprehensive Coverage**: The mock implementation allows us to test edge cases and error conditions that might be difficult to reproduce with real hardware.

5. **Regression Prevention**: Regular automated testing helps catch regressions early, ensuring that new changes don't break existing functionality.

The pipeline runs two test commands:
- `python -m unittest test.test_mock`: Specifically runs the mock tests
- `python -m unittest discover -s test`: Runs all tests (hardware tests are automatically skipped when hardware is not available)

This approach ensures that our library maintains compatibility with the SX126X hardware interface while allowing development and testing to proceed without physical hardware.
