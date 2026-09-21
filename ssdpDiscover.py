#!/usr/bin/env python3

"""Send an SSDP M-SEARCH probe and print the replies.

This is a small troubleshooting helper for multicast / SSDP environments.
"""

import argparse
import socket
import sys


def build_parser():
    parser = argparse.ArgumentParser(
        description="Send an SSDP M-SEARCH probe and print discovered devices.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--if-addr",
        "--ifAddr",
        dest="if_addr",
        help="Send the probe from the interface with this IPv4 address.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=2.0,
        help="How long to wait for replies after sending the probe.",
    )
    return parser


def main():
    args = build_parser().parse_args()

    msearch = (
        "M-SEARCH * HTTP/1.1\r\n"
        "HOST:239.255.255.250:1900\r\n"
        'ST:upnp:rootdevice\r\n'
        "MX:2\r\n"
        'MAN:"ssdp:discover"\r\n'
        "\r\n"
    )

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        if args.if_addr:
            sock.setsockopt(
                socket.IPPROTO_IP,
                socket.IP_MULTICAST_IF,
                socket.inet_aton(args.if_addr),
            )

        sock.settimeout(args.timeout)
        sock.sendto(msearch.encode("utf-8"), ("239.255.255.250", 1900))

        try:
            while True:
                data, addr = sock.recvfrom(65535)
                try:
                    host = socket.gethostbyaddr(addr[0])[0]
                    print(f"{host} [{addr[0]}]")
                except socket.herror:
                    print(addr[0])
                print(data.decode("utf-8", errors="replace"))
        except TimeoutError:
            return 0
        except KeyboardInterrupt:
            return 130


if __name__ == "__main__":
    sys.exit(main())
