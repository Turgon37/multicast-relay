# Changelog

All notable changes to the multicast relay are documented in this file.

Releases use Git tags in the `vMAJOR.MINOR.PATCH` format. A tag such as
`v1.2.3` publishes the Docker image with the same tag.

## [Unreleased]

No changes yet.

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
