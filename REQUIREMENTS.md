# Requirements for pysx126x

This document outlines the requirements for using and developing the pysx126x library.

## Python Requirements

- Python >= 3.8
- Compatible with Python 3.11 and 3.12

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- SX126X LoRa module (e.g., SX1262 868M LoRa HAT)
- Proper connections between the Raspberry Pi and SX126X module:
  - Default GPIO pin 6 for M0
  - Default GPIO pin 5 for M1
  - Serial connection (default: auto-detected)

## Software Dependencies

### Core Dependencies
- pyserial == 3.5
- RPi.GPIO == 0.7.1
- loguru >= 0.7.0

### Development Dependencies
- pytest >= 7.0.0
- pytest-cov >= 4.0.0
- build >= 1.0.0
- twine >= 4.0.0

## Operating System Requirements

- Linux-based operating system (primarily Raspberry Pi OS)
- User must have appropriate permissions:
  - Serial port access (member of 'dialout' group on Linux)
  - GPIO access (root privileges or member of 'gpio' group on Raspberry Pi)

## Testing Requirements

- Physical SX126X hardware connected to a Raspberry Pi is required for running tests
- Tests are not run in CI/CD pipelines due to hardware requirements
- Mock tests are available for development without hardware

## Additional Requirements

- For persistent configuration changes, set `write_persist=True` when making changes
- For debugging, set `debug=True` when initializing the SX126X class

## External Resources

- SX1262 868M LoRa HAT information: https://www.waveshare.com/wiki/SX1262_868M_LoRa_HAT
- LoRa HAT Register information: https://www.waveshare.com/wiki/LoRa-HAT-Reg
- LoRa HAT Control Protocol: https://www.waveshare.com/wiki/LoRa-HAT-Control