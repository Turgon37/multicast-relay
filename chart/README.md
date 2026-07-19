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

Set both `metrics.enabled` and `monitoring.podMonitor.enabled` to `true` to
create a Prometheus Operator `PodMonitor` targeting the relay's `/metrics`
endpoint.

`namespaceOverride` is optional. Leave it empty to use the Helm release namespace.
