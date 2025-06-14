# sx126x

## install

```shell
pip install sx126x
```

## development

For development setup and release process information, please see [CONTRIBUTING.md](CONTRIBUTING.md).

## defaults

| Parameter            | Default Value              | Description                                                           |
|----------------------|----------------------------|-----------------------------------------------------------------------|
| `address`            | `Address.parse("242.242")` | Device address                                                        |
| `net_id`             | `1`                        | Network ID                                                            |
| `channel`            | `1`                        | Channel                                                               |
| `port`               | `None`                     | Serial port path                                                      |
| `pin_m0`             | `6`                        | [GPIO 6](https://pinout.xyz/pinout/pin31_gpio6/) — Mode select pin M0 |
| `pin_m1`             | `5`                        | [GPIO 5](https://pinout.xyz/pinout/pin29_gpio5/) — Mode select pin M1 |
| `baud_rate`          | `BaudRate.B9600`           | UART baud rate                                                        |
| `byte_size`          | `8`                        | Number of data bits                                                   |
| `parity`             | `Parity.NONE`              | Parity bit setting                                                    |
| `stop_bits`          | `1`                        | Number of stop bits                                                   |
| `write_persist`      | `False`                    | Write registers persistently                                          |
| `mode`               | `Mode.CONFIGURATION`       | Set M0 and M1 according to mode                                       |
| `timeout`            | `2`                        | Read/write timeout in seconds                                         |
| `debug`              | `False`                    | Enable debug logging                                                  |
| `air_speed`          | `AirSpeed.K2_4`            | Air data rate                                                         |
| `packet_size`        | `PacketSize.SIZE_128`      | Packet size                                                           |
| `ambient_noise`      | `AmbientNoise.DISABLED`    | Ambient noise detection mode                                          |
| `transmit_power`     | `TransmitPower.DBM_22`     | RF transmit power                                                     |
| `rssi`               | `RSSI.DISABLED`            | Add RSSI to RX data                                                   |
| `transfer_method`    | `TransferMethod.FIXED`     | Transmission addressing mode                                          |
| `relay`              | `Relay.DISABLED`           | Enable or disable relay functionality                                 |
| `lbt`                | `LBT.DISABLED`             | Listen Before Talk mode                                               |
| `wor_control`        | `WORControl.TRANSMIT`      | WOR (Wake On Radio) mode control                                      |
| `wor_period`         | `WORPeriod.MS_500`         | WOR cycle period                                                      |
| `crypt_key`          | `CryptKey(0, 0)`           | 16-bit encryption key                                                 |
| `overwrite_defaults` | `True`                     | Whether to override internal default parameters                       |


## features

- [X] mock interface for testing without hardware
- [ ] configuration
  - [X] address
    - [X] hi
    - [X] lo
    - [X] hi:lo
  - [X] net id
  - [X] baud rate
  - [X] parity
  - [X] air speed
  - [X] ambient noise
  - [X] transmit power
  - [X] channel
  - [X] rssi
  - [X] transfer mode
  - [X] lbt
  - [X] wor control
  - [X] wor period
  - [?] crypt key (data does not persist?)
    - [?] hi
    - [?] lo
    - [?] hilo
  - [ ] module info
- [X] mode switching
- [X] rx (& rx loop)
- [X] tx
- [X] tests
- [ ] documentation
- [ ] examples
  - [X] defaults
  - [X] rx
  - [X] tx
  - [X] mock
  - [ ] configuration (look at tests for now)

## examples

### mock interface

The `MockSX126X` class provides a mock implementation of the SX126X interface for testing without requiring the actual hardware. It simulates the bit-encoded properties and register behavior of the SX1262 device.

This class is available in the test directory and is not part of the public API. It is intended for testing purposes only.

For examples of how to use the mock interface, see the `test/mock_example.py` file.

### sender

```python
from sx126x import SX126X, Address

lora = SX126X(Address(3, 4))
lora.tx(Address(6, 9), b"DIE")
```

### receiver

```python
from sx126x import SX126X, Address

lora = SX126X(Address(6, 9))
address, data = lora.rx()
# or
def lora_cb(address: Address, data: bytes) -> bool:
  if address.__str__() == "3.4" and data == b"DIE":
    return False  # stop receiving
  return True  # continue receiving
lora.rx_loop(lora_cb)
```
