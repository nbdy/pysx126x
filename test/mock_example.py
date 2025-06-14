from time import sleep
from pprint import pprint

from sx126x import Address, Mode, AirSpeed, TransmitPower
from test.mock_sx126x import MockSX126X


def main():
    # Create two mock devices
    print("Creating mock devices...")
    device1 = MockSX126X(
        address=Address.parse("242.242"),
        net_id=1,
        channel=1,
        debug=True
    )

    device2 = MockSX126X(
        address=Address.parse("242.243"),
        net_id=1,
        channel=1,
        debug=True
    )

    # Print initial configuration
    print("\nDevice 1 configuration:")
    pprint(device1.to_json())

    print("\nDevice 2 configuration:")
    pprint(device2.to_json())

    # Change some settings
    print("\nChanging device 1 settings...")
    device1.air_speed = AirSpeed.K9_6
    device1.transmit_power = TransmitPower.DBM_17

    # Print updated configuration
    print("\nDevice 1 updated configuration:")
    pprint(device1.to_json())

    # Set both devices to transmission mode
    device1.set_mode(Mode.TRANSMISSION)
    device2.set_mode(Mode.TRANSMISSION)

    # Simulate device1 sending a message to device2
    print("\nSimulating transmission from device1 to device2...")
    device1.tx(device2.address, b"Hello from device1!")

    # In a real scenario, device2 would receive this over the air
    # For our mock, we need to manually simulate the reception
    device2.simulate_receive(device1.address, b"Hello from device1!")

    # Device2 receives the message
    print("\nDevice2 receiving message...")
    received = device2.rx()
    if received:
        addr, data = received
        print(f"Received from {addr}: {data.decode()}")
    else:
        print("No data received")

    # Demonstrate rx_loop
    print("\nDemonstrating rx_loop...")

    # Simulate multiple messages
    device2.simulate_receive(device1.address, b"Message 1")
    device2.simulate_receive(device1.address, b"Message 2")
    device2.simulate_receive(device1.address, b"Message 3")

    # Counter for received messages
    message_count = 0

    # Callback function for rx_loop
    def rx_callback(address, data):
        nonlocal message_count
        message_count += 1
        print(f"Callback received from {address}: {data.decode()}")
        # Stop after receiving 3 messages
        return message_count < 3

    # Start rx_loop in a separate thread (for demo purposes, we'll use a simple approach)
    import threading
    rx_thread = threading.Thread(target=device2.rx_loop, args=(rx_callback,))
    rx_thread.daemon = True
    rx_thread.start()

    # Wait for all messages to be processed
    sleep(1)

    print("\nDemo completed!")


if __name__ == "__main__":
    main()