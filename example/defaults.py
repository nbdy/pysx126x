from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pprint import pprint

from sx126x import SX126X, Mode


def main():
    ap = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    ap.add_argument("-p", "--port", default=None, type=str, help="Serial port")
    ap.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = ap.parse_args()

    lora = SX126X(
        port=args.port,
        debug=args.debug,
        overwrite_defaults=False
    )
    pprint(lora.to_json())


if __name__ == '__main__':
    main()
