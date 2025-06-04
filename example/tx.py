from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pprint import pprint
from time import sleep

from sx126x import SX126X, Mode, Address


def main():
    ap = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    ap.add_argument("-p", "--port", default=None, type=str, help="Serial port")
    ap.add_argument("-t", "--text", default="Hello World", type=str, help="Text to send")
    ap.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    ap.add_argument("-ta", "--tx-addr", default="242.242", type=str, help="TX address")
    ap.add_argument("-ra", "--rx-addr", default="242.242", type=str, help="RX address")
    ap.add_argument("-c", "--channel", default=1, type=int, help="Channel")
    ap.add_argument("-n", "--net-id", default=1, type=int, help="Network ID")
    args = ap.parse_args()

    lora = SX126X(
        address=Address.parse(args.tx_addr),
        net_id=args.net_id,
        channel=args.channel,
        port=args.port,
        debug=args.debug
    )
    pprint(lora.to_json())

    lora.set_mode(Mode.TRANSMISSION)

    do_run = True

    rx_addr = Address.parse(args.rx_addr)

    print(f"Sending '{args.text}'...")
    while do_run:
        try:
            lora.tx(rx_addr, args.text.encode())
            sleep(1)
        except KeyboardInterrupt:
            print("Stopping...")
            do_run = False


if __name__ == '__main__':
    main()
