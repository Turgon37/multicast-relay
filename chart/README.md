# multicast-relay

Deploy the relay in the target namespace with:

```sh
helm upgrade --install multicast-relay ./chart --namespace prod-multicastrelay --create-namespace
```

Configure `relay.interfaces`, `relay.remote`, the boolean relay options,
`livenessPort`, probes, image, security context and resources in `values.yaml`
or with an additional values file. `--k8sport` is generated from
`livenessPort`; do not add it to `relay.extraArgs`.

`relay.interfaces` has no default and is required. `relay.remote` is optional;
when `relay.remote.addresses` is configured, `relay.remote.port` is required.
The `chart/ci/lint-values.yaml` file supplies a placeholder interface for CI
linting only and must not be used for deployment.

Enable `networkPolicy` with the `kubernetes` or `cilium` flavor and provide its
ingress/egress rules when network isolation is required.

Set both `metrics.enabled` and `metrics.podMonitor.enabled` to `true` to
create a Prometheus Operator `PodMonitor` targeting the relay's `/metrics`
endpoint.

`namespaceOverride` is optional. Leave it empty to use the Helm release namespace.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `nameOverride` | string | `""` | Overrides the chart name used in resource names and labels. |
| `fullnameOverride` | string | `""` | Fully overrides the generated release resource name. |
| `namespaceOverride` | string | `""` | Overrides the Helm release namespace for chart resources. |
| `replicaCount` | int | `1` | Number of relay pods. Use `1` when host networking shares the same interface. |
| `strategy.type` | string | `"Recreate"` | Deployment strategy; `Recreate` or `RollingUpdate`. |
| `image.repository` | string | `"ghcr.io/turgon37/multicast-relay"` | Container image repository. |
| `image.tag` | string | `"1.0.0"` | Container image tag. |
| `image.pullPolicy` | string | `"IfNotPresent"` | Kubernetes image pull policy. |
| `relay.interfaces` | list | `[]` | Required interfaces passed to `--interfaces`. |
| `relay.noTransmitInterfaces` | list | `[]` | Listen-only interfaces passed to `--noTransmitInterfaces`. |
| `relay.remote.addresses` | list | `[]` | Remote relay addresses passed to `--remote`. |
| `relay.remote.port` | int or null | `null` | Required remote relay port when `relay.remote.addresses` is set. |
| `relay.wait` | bool | `false` | Adds `--wait` to wait for interface IPv4 addresses. |
| `relay.transmitUdp` | bool | `false` | Adds `--transmitUdp` instead of using raw sockets for transmission. |
| `relay.noRemoteRelay` | bool | `false` | Adds `--noRemoteRelay`. |
| `relay.verbose` | bool | `false` | Adds `--verbose`. |
| `relay.debug` | bool | `false` | Adds `--debug`. |
| `relay.extraArgs` | list | `[]` | Additional relay command-line arguments not exposed as dedicated values. |
| `livenessPort` | int | `10015` | Port used for `--k8sport` and HTTP liveness/readiness probes. |
| `metrics.enabled` | bool | `false` | Adds `--metrics-port` and exposes the named container port `metrics`. |
| `metrics.port` | int | `9090` | Prometheus metrics port. |
| `metrics.podMonitor.enabled` | bool | `false` | Creates a Prometheus Operator `PodMonitor`; requires `metrics.enabled`. |
| `metrics.podMonitor.namespace` | string | `""` | Namespace containing the `PodMonitor`; defaults to the release namespace. |
| `metrics.podMonitor.labels` | object | `{}` | Additional labels for the `PodMonitor`. |
| `metrics.podMonitor.interval` | string | `"15s"` | Prometheus scrape interval. |
| `metrics.podMonitor.scrapeTimeout` | string | `""` | Optional Prometheus scrape timeout. |
| `metrics.podMonitor.path` | string | `"/metrics"` | Metrics HTTP path. |
| `env` | object | `{"TZ":"Europe/Paris"}` | Environment variables added to the relay container. |
| `extraEnv` | list | `[]` | Additional complete Kubernetes environment variable entries. |
| `hostNetwork` | bool | `true` | Enables host networking for multicast packet reception and emission. |
| `dnsPolicy` | string | `"ClusterFirstWithHostNet"` | Pod DNS policy. |
| `terminationGracePeriodSeconds` | int | `30` | Grace period Kubernetes gives the relay after `SIGTERM`. |
| `podAnnotations` | object | `{}` | Annotations added to the pod. |
| `podLabels` | object | `{}` | Labels added to the pod. |
| `containerSecurityContext` | object | `{"capabilities":{"add":["NET_RAW","NET_ADMIN"]}}` | Container security context; raw socket capabilities are required by the default transport. |
| `resources` | object | `{}` | Kubernetes resource requests and limits. |
| `probes.liveness.enabled` | bool | `true` | Enables the HTTP liveness probe on `livenessPort`. |
| `probes.liveness.path` | string | `"/"` | Liveness probe HTTP path. |
| `probes.liveness.initialDelaySeconds` | int | `10` | Delay before the liveness probe starts. |
| `probes.liveness.periodSeconds` | int | `10` | Liveness probe period. |
| `probes.liveness.timeoutSeconds` | int | `2` | Liveness probe timeout. |
| `probes.liveness.successThreshold` | int | `1` | Consecutive liveness successes required. |
| `probes.liveness.failureThreshold` | int | `3` | Consecutive liveness failures before restart. |
| `probes.readiness.enabled` | bool | `false` | Enables the HTTP readiness probe on `livenessPort`. |
| `probes.readiness.path` | string | `"/"` | Readiness probe HTTP path. |
| `probes.readiness.initialDelaySeconds` | int | `10` | Delay before the readiness probe starts. |
| `probes.readiness.periodSeconds` | int | `10` | Readiness probe period. |
| `probes.readiness.timeoutSeconds` | int | `2` | Readiness probe timeout. |
| `probes.readiness.successThreshold` | int | `1` | Consecutive readiness successes required. |
| `probes.readiness.failureThreshold` | int | `3` | Consecutive readiness failures before unready. |
| `nodeSelector` | object | `{}` | Node selector for pod scheduling. |
| `tolerations` | list | `[]` | Tolerations for pod scheduling. |
| `affinity` | object | `{}` | Affinity and anti-affinity rules. |
| `networkPolicy.enabled` | bool | `false` | Creates a network policy for the relay pods. |
| `networkPolicy.flavor` | string | `"kubernetes"` | Policy implementation: `kubernetes` or `cilium`. |
| `networkPolicy.policyTypes` | list | `[]` | Explicit Kubernetes policy types; inferred from ingress/egress when empty. |
| `networkPolicy.ingress` | list | `[]` | Kubernetes `NetworkPolicy` ingress rules. |
| `networkPolicy.egress` | list | `[]` | Kubernetes `NetworkPolicy` egress rules. |
| `networkPolicy.cilium.ingress` | list | `[]` | Cilium ingress rules. |
| `networkPolicy.cilium.egress` | list | `[]` | Cilium egress rules. |
| `networkPolicy.cilium.enableDefaultDeny` | object | `{}` | Cilium default-deny settings; Cilium requires at least one rule or this setting when enabled. |
