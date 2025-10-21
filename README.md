# sx126x

A Python library for interfacing with SX126X LoRa modules. This library provides a simple API for configuring and using SX126X devices for wireless communication.

## Hardware Requirements

This library is designed to work with SX126X LoRa modules connected to a Raspberry Pi. The default configuration assumes the module is connected to GPIO pins 5 and 6 for mode control, but this can be customized.

## Installation

**Using pip:**
```shell
pip install sx126x
```

**Using uv:**
```shell
uv pip install sx126x
```

For more information about uv, see https://docs.astral.sh/uv/

## Default Configuration

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


## Usage Examples

The following examples demonstrate how to use the SX126X library for basic sending and receiving operations.

### Sender

```python
from sx126x import SX126X, Address

lora = SX126X(Address(3, 4))
lora.tx(Address(6, 9), b"Hello from device 3.4")
```

### Receiver

```python
from sx126x import SX126X, Address

lora = SX126X(Address(6, 9))
address, data = lora.rx()
# or
def lora_cb(address: Address, data: bytes) -> bool:
  if address.__str__() == "3.4" and data == b"Hello from device 3.4":
    print(f"Received message: {data.decode()}")
    return False  # stop receiving
  return True  # continue receiving
lora.rx_loop(lora_cb)
```
