# Changelog

All notable changes to the multicast relay are documented in this file.

Releases use Git tags in the `vMAJOR.MINOR.PATCH` format. A tag such as
`v1.2.3` publishes the Docker image with the same tag.

## [Unreleased]

- Add configurable Helm deployment with host networking, Kubernetes liveness,
  graceful signal handling, NetworkPolicy and CiliumNetworkPolicy support.
- Add optional Prometheus metrics and Prometheus Operator `PodMonitor` support.
- Add UDP socket transmission mode with loop prevention for locally emitted
  packets.
- Add tcpdump-like packet debugging and remote forwarding diagnostics.
- Add Alpine-based Docker image, Helm OCI publication and Cosign signatures.

