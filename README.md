Relay broadcast and multicast packets between interfaces
--------------------------------------------------------

[![CI](https://github.com/Turgon37/multicast-relay/actions/workflows/ci.yml/badge.svg)](https://github.com/Turgon37/multicast-relay/actions/workflows/ci.yml)
[![Chart CI](https://github.com/Turgon37/multicast-relay/actions/workflows/chart-ci.yml/badge.svg)](https://github.com/Turgon37/multicast-relay/actions/workflows/chart-ci.yml)
[![Docker image](https://github.com/Turgon37/multicast-relay/actions/workflows/docker-image.yml/badge.svg)](https://github.com/Turgon37/multicast-relay/actions/workflows/docker-image.yml)
[![Helm chart](https://github.com/Turgon37/multicast-relay/actions/workflows/helm-chart.yml/badge.svg)](https://github.com/Turgon37/multicast-relay/actions/workflows/helm-chart.yml)
[![License](https://img.shields.io/github/license/Turgon37/multicast-relay)](https://github.com/Turgon37/multicast-relay/blob/master/LICENSE)

See the [changelog](CHANGELOG.md) for the relay history and release notes.

## Delivery

Releases are published from `master` only.

- Pull requests run validation through `CI` and `Chart CI`.
- Merges to `master` can publish the Docker image and Helm chart automatically.
- Each publication also creates a GitHub Release: `v<image-version>` for Docker and `chart-v<chart-version>` for the Helm chart.
- The Docker image is pushed to GHCR and signed with Cosign.
- The Helm chart is packaged as an OCI artifact on GHCR, signed with Cosign, published with Artifact Hub metadata, and the GitHub Release carries signed release metadata and the packaged chart asset signature.
- Renovate opens dependency update PRs but does not publish releases.
- The Docker image also ships `ssdp-discover` as a small SSDP/multicast debug helper.

Recommended GitHub branch protection for `master`:

- Require pull requests before merging.
- Require at least one review.
- Require review approval from code owners.
- Dismiss stale approvals when new commits are pushed.
- Require status checks to pass before merging.
- Require the `CI` check.
- Require the `Chart CI` check.
- Restrict who can push to `master`.
- Disable force pushes.
- Optionally require linear history.

Useful, for example, if you have Sonos speakers on one interface, or VLAN,
and you want to be able to control them from devices on a different
interface/VLAN. Similar for Chromecast devices.

By default, SSDP multicast packets received on 239.255.255.250:1900 are
relayed to the other interfaces listed, as well as multicast DNS packets
received on 224.0.0.251:5353.

Broadcast UDP packets received on port 6969 are also relayed by default:
this is used by Sonos during the initial device-discovery phase, initiated
by pressing either the infinity button or the play+volume up buttons,
depending on your Sonos speaker.

Please note that even when your devices have discovered one another, at
least in the Sonos case, a unicast connection will be established from
the speakers back to the controlling-telephone. You will need to make sure
that IP forwarding is enabled (`echo 1 > /proc/sys/net/ipv4/ip_forward`) and
that no firewalling is in place that would prevent connections being
established.

`usage: multicast-relay.py [-h] --interfaces INTERFACE INTERFACE [INTERFACE ...] [--noTransmitInterfaces INTERFACE ...] [-ifFilter IFFILTER] [--relay BROADCAST_OR_MULTICAST:PORT [BROADCAST_OR_MULTICAST:PORT ...]] [--noMDNS] [--noSSDP] [--noSonosDiscovery] [--oneInterface] [--homebrewNetifaces] [--transmitUdp] [--receiveUdp] [--receiveLocalOutgoing] [--wait] [--listen REMOTE_ADDRESS [REMOTE_ADDRESS ...]] [--remote REMOTE_ADDRESS] [--remotePort PORT] [--remoteRetry SECS] [--metrics-port PORT] [--foreground] [--logfile FILE] [--verbose] [--debug]`

`--interfaces` specifies the >= 2 interfaces that you desire to listen to and
relay between. You can specify an interface by name, by IP address, or by
network/netmask combination (e.g. 10.0.0.0/24 in the last case). With certain
flags below, the minimum number of interfaces drops to >= 1.

`--noTransmitInterfaces` specifies interface(s) that are listen-only.

`--ifFilter` specifies a JSON file where one can state that a source address
A.B.C.D/M is only to be relayed to specific interfaces. This can be useful
in applications such as a hotel where relaying for one guest room may only
discover device(s) that are in the same guest room. See example file
[`examples/ifFilter.json`](examples/ifFilter.json).

`--relay` specifies additional broadcast or multicast addresses to relay.

`--noMDNS` disables mDNS relaying.

`--noSSDP` disables SSDP relaying.

`--noSonosDiscovery` disables broadcast udp/6969 relaying.

`--oneInterface` support for one interface connected to two networks. Use with
caution - watch out for packet storms (although the IP checksum list ought
to still prevent such a thing from happening).

`--homebrewNetifaces` attempt to use our own netifaces implementation, probably
doesn't work on any other system than Linux but maybe useful for OpenWRT where
it's rather tricky to compile up netifaces.

`--allowNonEther` supports non-ethernet interfaces to be relayed [experimental].

`--transmitUdp` sends relayed packets through UDP sockets instead of raw packet sockets. The outgoing socket is bound to the transmitting interface IP, so that IP is used as the source and the operating system selects the source port; the original source address and port are not preserved.

`--receiveUdp` receives multicast packets through UDP sockets instead of raw packet sockets. The relay rebuilds an IPv4 UDP packet from the received payload, source address and source port before applying the existing forwarding logic. This mode is useful when the kernel does not deliver the expected multicast traffic to the historical raw IPv4 receive socket.

`--receiveLocalOutgoing` receives locally generated multicast packets through AF_PACKET sockets. The socket filter keeps only locally emitted UDP packets matching configured multicast relay destinations, then the relay decapsulates the Ethernet frame back to IPv4 and reuses the existing forwarding logic. This is the mode to enable when a local process on the same host emits multicast, the packet is visible on the wire, but neither the raw IPv4 listener nor `--receiveUdp` see it.

The receive and transmit options are independent:

- Default mode: raw IPv4 receive and raw packet transmit. This preserves the historical behavior.
- `--receiveUdp`: use UDP multicast sockets for packets received from the network.
- `--receiveLocalOutgoing`: add AF_PACKET listeners for locally generated multicast packets only.
- `--transmitUdp`: transmit relayed traffic with UDP sockets instead of raw Ethernet sockets.

For a host that must relay both multicast coming from the network and multicast generated locally by another process on the same machine, the expected setup is typically `--receiveUdp --receiveLocalOutgoing`. `--receiveUdp` handles inbound multicast received from the network and `--receiveLocalOutgoing` handles `PACKET_OUTGOING` traffic generated by the local host.

`--wait` indicates that the relay should wait for an IPv4 address to be assigned
to each interface rather than bailing immediately if an interface is yet to be
assigned an address.

`--listen` for connections from the specified remote host(s) or network(s), for example `--listen 10.0.0.1 192.168.0.0/16`.

`--remote` connect to the specified remote host. If either --listen or --remote
are specified, then one can also specify just one local interface with --interfaces.

`--remotePort` use the specified port for remote communications (default: 1900).

`--remoteRetry` if the remote connection fails, wait at least this number of seconds before retrying (default: 5).

`--aes` use the specified string to encrypt/decrypt data packets.

`--metrics-port` exposes Prometheus metrics on `/metrics` at the specified port. The container image includes the required `prometheus-client` package. In addition to packet counters, the relay exports cumulative CPU time spent processing packets with the `multicast_relay_packet_processing_cpu_seconds_total{source=...}` metric, labelled by packet source (`remote`, `local_raw`, `local_udp`, `local_outgoing`).

`--foreground` stops the process forking itself off into the background. This
flag also encourages logging to stdout as well as to the syslog.

`--logfile` saves log data to the specified file.

`--verbose` steps up the logging.

`--debug` logs a tcpdump-like description of every packet received by the relay. Use it with `--foreground` to print the diagnostics to standard output.

multicast-relay.py requires the python 'netifaces' package. Install via
'easy_install netifaces' or 'pip install netifaces'. For ZeroShell users,
please review [README-ZeroShell](docs/legacy/README-ZeroShell.md) for further instructions.

Al Smith <ajs@aeschi.eu>
