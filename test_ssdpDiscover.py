import socket
import sys

import ssdpDiscover as sd


def test_build_parser_accepts_legacy_interface_flag():
    parser = sd.build_parser()
    args = parser.parse_args(["--ifAddr", "10.0.0.1", "--timeout", "1.5"])

    assert args.if_addr == "10.0.0.1"
    assert args.timeout == 1.5


def test_main_sends_probe_and_prints_response(monkeypatch, capsys):
    class FakeSocket:
        def __init__(self):
            self.options = []
            self.timeout = None
            self.sent = None
            self.calls = 0

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def setsockopt(self, level, option, value):
            self.options.append((level, option, value))

        def settimeout(self, value):
            self.timeout = value

        def sendto(self, data, destination):
            self.sent = (data, destination)

        def recvfrom(self, size):
            self.calls += 1
            if self.calls == 1:
                return (
                    b"HTTP/1.1 200 OK\r\nST:upnp:rootdevice\r\n\r\n",
                    ("192.0.2.15", 1900),
                )
            raise TimeoutError()

    fake_socket = FakeSocket()
    monkeypatch.setattr(sd.socket, "socket", lambda *args, **kwargs: fake_socket)
    monkeypatch.setattr(sd.socket, "gethostbyaddr", lambda addr: ("device.local", [], [addr]))
    monkeypatch.setattr(sys, "argv", ["ssdpDiscover.py", "--if-addr", "10.0.0.1", "--timeout", "0.1"])

    assert sd.main() == 0

    output = capsys.readouterr().out
    assert fake_socket.timeout == 0.1
    assert fake_socket.sent == (
        b"M-SEARCH * HTTP/1.1\r\nHOST:239.255.255.250:1900\r\nST:upnp:rootdevice\r\nMX:2\r\nMAN:\"ssdp:discover\"\r\n\r\n",
        ("239.255.255.250", 1900),
    )
    assert fake_socket.options == [
        (socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton("10.0.0.1"))
    ]
    assert "device.local [192.0.2.15]" in output
    assert "HTTP/1.1 200 OK" in output


def test_main_returns_130_on_keyboard_interrupt(monkeypatch):
    class FakeSocket:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def settimeout(self, value):
            pass

        def sendto(self, data, destination):
            pass

        def recvfrom(self, size):
            raise KeyboardInterrupt()

    monkeypatch.setattr(sd.socket, "socket", lambda *args, **kwargs: FakeSocket())
    monkeypatch.setattr(sys, "argv", ["ssdpDiscover.py"])

    assert sd.main() == 130
