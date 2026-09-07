# Changelog

All notable changes to the multicast relay are documented in this file.

Releases use Git tags in the `vMAJOR.MINOR.PATCH` format. A tag such as
`v1.2.3` publishes the Docker image with the same tag.

## [Unreleased]

No changes yet.

## [0.1.23] - 2026-09-07

Chart version `0.1.23`, using multicast-relay image version `1.0.6`.

- Restrict raw broadcast listeners to their configured broadcast destination so they do not also process multicast packets received on the same UDP port.
- Fix the `--receiveLocalOutgoing` socket filter program so it attaches cleanly on Linux packet sockets.

## [0.1.22] - 2026-09-07

Chart version `0.1.22`, using multicast-relay image version `1.0.5`.

- Open one UDP multicast receive socket per interface when `--receiveUdp` is enabled instead of sharing a single socket across interfaces.
- Preserve the receiving interface metadata in `receiveUdp` mode so packets are not needlessly retransmitted back onto their source interface.
- Restrict raw broadcast listeners to their configured broadcast destination so they do not also process multicast packets received on the same UDP port.

## [0.1.21] - 2026-09-07

Chart version `0.1.21`, using multicast-relay image version `1.0.4`.

- Rename the local AF_PACKET receive option to `--receiveLocalOutgoing` and update the Helm value to `relay.receiveLocalOutgoing`.
- Document how the receive and transmit socket modes work and when to use each option.
- Export cumulative CPU time spent processing packets with Prometheus labels per packet source.

## [0.1.20] - 2026-09-07

Chart version `0.1.20`, using multicast-relay image version `1.0.3`.

- Add AF_PACKET-based capture for locally generated multicast packets with a kernel socket filter.
- Expose the `receiveOutgoing` relay option in the Helm chart values and deployment template.
- Apply the configured timezone to log timestamps and include timezone data in the container image.

## [0.1.19] - 2026-09-06

Chart version `0.1.19`, using multicast-relay image version `1.0.2`.

- Add startup logs showing the receive socket type configured for each relay listener.
- Add startup logs showing the transmit socket type configured for each interface.

## [0.1.18] - 2026-09-06

Chart version `0.1.18`, using multicast-relay image version `1.0.1`.

- Align the chart with the application image version that includes the `--receiveUdp` option.
- Default the chart image tag and metadata to multicast-relay `1.0.1`.

## [0.1.17] - 2026-09-05

Chart version `0.1.17`, using multicast-relay image version `1.0.0`.

- Add the `--receiveUdp` option to receive multicast packets through UDP sockets.
- Expose the `receiveUdp` relay option in the Helm chart values and deployment template.

## [0.1.16] - 2026-08-11

Chart version `0.1.16`, using multicast-relay image version `1.0.0`.

- Stop publishing the Helm chart repository on GitHub Pages.
- Publish the Helm chart exclusively as an OCI artifact on GHCR.

## [0.1.15] - 2026-07-21

Chart version `0.1.15`, using multicast-relay image version `1.0.0`.

- Add configurable Helm deployment with host networking, Kubernetes liveness,
  graceful signal handling, NetworkPolicy and CiliumNetworkPolicy support.
- Add optional Prometheus metrics and Prometheus Operator `PodMonitor` support.
- Add UDP socket transmission mode with loop prevention for locally emitted
  packets.
- Add tcpdump-like packet debugging and remote forwarding diagnostics.
- Add Alpine-based Docker image, Helm OCI publication and Cosign signatures.
- Add GitHub Pages HTTP Helm repository and Artifact Hub metadata.
- Add Artifact Hub links, container image metadata and per-release changes.
