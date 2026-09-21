# multicast-relay

![Version: 0.1.28](https://img.shields.io/badge/Version-0.1.28-informational?style=flat-square)
![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square)
![AppVersion: 1.0.9](https://img.shields.io/badge/AppVersion-1.0.9-informational?style=flat-square)

Relay multicast and broadcast UDP packets between networks.

## Installing the Chart

The chart is published only as an OCI artifact on GHCR.

Install the chart with the release name `multicast-relay` from GHCR:

```console
helm upgrade --install multicast-relay \
  oci://ghcr.io/turgon37/charts/multicast-relay \
  --namespace prod-multicastrelay \
  --create-namespace \
  --version 0.1.28 \
  --set relay.interfaces[0]=eth0
```

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

Set `grafanaDashboard.enabled` to `true` to create a ConfigMap containing a
Grafana dashboard for the relay metrics. The ConfigMap is labeled for common
Grafana sidecar loaders and the label key/value, namespace, labels and
annotations are configurable.

`namespaceOverride` is optional. Leave it empty to use the Helm release namespace.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity and anti-affinity rules. |
| containerSecurityContext.capabilities.add[0] | string | `"NET_RAW"` | Required by raw sockets. |
| containerSecurityContext.capabilities.add[1] | string | `"NET_ADMIN"` | Required to allow multicast socket configuration on some systems. |
| dnsPolicy | string | `"ClusterFirstWithHostNet"` | Pod DNS policy. |
| env.TZ | string | `"Europe/Paris"` | Environment variables added to the relay container. |
| extraEnv | list | `[]` | Additional complete Kubernetes environment variable entries. |
| fullnameOverride | string | `""` | Fully overrides the generated release resource name. |
| grafanaDashboard.annotations | object | `{}` | Additional annotations for the dashboard ConfigMap. |
| grafanaDashboard.enabled | bool | `false` | Creates a ConfigMap containing a Grafana dashboard for multicast-relay metrics. |
| grafanaDashboard.labels | object | `{}` | Additional labels for the dashboard ConfigMap. |
| grafanaDashboard.namespace | string | `""` | Namespace containing the dashboard ConfigMap; defaults to the release namespace. |
| grafanaDashboard.sidecarLabel | string | `"grafana_dashboard"` | Label key used by Grafana sidecar dashboard loaders. |
| grafanaDashboard.sidecarLabelValue | string | `"1"` | Label value used by Grafana sidecar dashboard loaders. |
| hostNetwork | bool | `true` | Enables host networking for multicast packet reception and emission. |
| image.pullPolicy | string | `"IfNotPresent"` | Kubernetes image pull policy. |
| image.repository | string | `"ghcr.io/turgon37/multicast-relay"` | Container image repository. |
| image.tag | string | `"1.0.9"` | Container image tag. |
| livenessPort | int | `10015` | Port used for the k8sport HTTP endpoint and HTTP liveness/readiness probes. |
| metrics.enabled | bool | `false` | Enables the metrics port and exposes the named container port metrics. |
| metrics.podMonitor.enabled | bool | `false` | Creates a Prometheus Operator PodMonitor; requires metrics.enabled. |
| metrics.podMonitor.interval | string | `"15s"` | Prometheus scrape interval. |
| metrics.podMonitor.labels | object | `{}` | Additional labels for the PodMonitor. |
| metrics.podMonitor.namespace | string | `""` | Namespace containing the PodMonitor; defaults to the release namespace. |
| metrics.podMonitor.path | string | `"/metrics"` | Metrics HTTP path. |
| metrics.podMonitor.scrapeTimeout | string | `""` | Optional Prometheus scrape timeout. |
| metrics.port | int | `9090` | Prometheus metrics port. |
| nameOverride | string | `""` | Overrides the chart name used in resource names and labels. |
| namespaceOverride | string | `""` | Overrides the Helm release namespace for chart resources. |
| networkPolicy.cilium.egress | list | `[]` | Cilium egress rules. |
| networkPolicy.cilium.enableDefaultDeny | object | `{}` | Cilium default-deny settings. |
| networkPolicy.cilium.ingress | list | `[]` | Cilium ingress rules. |
| networkPolicy.egress | list | `[]` | Kubernetes NetworkPolicy egress rules. |
| networkPolicy.enabled | bool | `false` | Creates a network policy for the relay pods. |
| networkPolicy.flavor | string | `"kubernetes"` | Policy implementation: kubernetes or cilium. |
| networkPolicy.ingress | list | `[]` | Kubernetes NetworkPolicy ingress rules. |
| networkPolicy.policyTypes | list | `[]` | Explicit Kubernetes policy types; inferred from ingress/egress when empty. |
| nodeSelector | object | `{}` | Node selector for pod scheduling. |
| podAnnotations | object | `{}` | Annotations added to the pod. |
| podLabels | object | `{}` | Labels added to the pod. |
| probes.liveness.enabled | bool | `true` | Enables the HTTP liveness probe on livenessPort. |
| probes.liveness.failureThreshold | int | `3` | Consecutive liveness failures before restart. |
| probes.liveness.initialDelaySeconds | int | `10` | Delay before the liveness probe starts. |
| probes.liveness.path | string | `"/"` | Liveness probe HTTP path. |
| probes.liveness.periodSeconds | int | `10` | Liveness probe period. |
| probes.liveness.successThreshold | int | `1` | Consecutive liveness successes required. |
| probes.liveness.timeoutSeconds | int | `2` | Liveness probe timeout. |
| probes.readiness.enabled | bool | `false` | Enables the HTTP readiness probe on livenessPort. |
| probes.readiness.failureThreshold | int | `3` | Consecutive readiness failures before unready. |
| probes.readiness.initialDelaySeconds | int | `10` | Delay before the readiness probe starts. |
| probes.readiness.path | string | `"/"` | Readiness probe HTTP path. |
| probes.readiness.periodSeconds | int | `10` | Readiness probe period. |
| probes.readiness.successThreshold | int | `1` | Consecutive readiness successes required. |
| probes.readiness.timeoutSeconds | int | `2` | Readiness probe timeout. |
| relay.debug | bool | `false` | Adds the debug flag. |
| relay.extraArgs | list | `[]` | Additional relay arguments not exposed as dedicated values. |
| relay.interfaces | list | `[]` | Required interfaces passed to the interfaces flag. |
| relay.noRemoteRelay | bool | `false` | Adds the noRemoteRelay flag. |
| relay.noTransmitInterfaces | list | `[]` | Listen-only interfaces passed to the noTransmitInterfaces flag. |
| relay.receiveLocalOutgoing | bool | `false` | Adds the receiveLocalOutgoing flag to receive locally generated multicast traffic through AF_PACKET sockets. |
| relay.receiveUdp | bool | `false` | Adds the receiveUdp flag to receive multicast traffic through UDP sockets. |
| relay.remote.addresses | list | `[]` | Remote relay addresses passed to the remote flag. |
| relay.remote.port | string | `nil` | Required remote relay port when remote addresses are set. |
| relay.transmitUdp | bool | `false` | Adds the transmitUdp flag instead of using raw sockets for transmission. |
| relay.verbose | bool | `false` | Adds the verbose flag. |
| relay.wait | bool | `false` | Adds the wait flag to wait for interface IPv4 addresses. |
| replicaCount | int | `1` | Number of relay pods. Use 1 when host networking shares the same interface. |
| resources | object | `{}` | Kubernetes resource requests and limits. |
| strategy.type | string | `"Recreate"` | Deployment strategy: Recreate or RollingUpdate. |
| terminationGracePeriodSeconds | int | `30` | Grace period Kubernetes gives the relay after SIGTERM. |
| tolerations | list | `[]` | Tolerations for pod scheduling. |
