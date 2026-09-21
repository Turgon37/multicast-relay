# Repository instructions

## Helm chart changes

- Treat every change under `chart/` that affects the packaged chart as a chart
  release change.
- Increment `version` in `chart/Chart.yaml` before publishing a modified chart.
- Helm publishing is blocked until `chart/Chart.yaml:version` changes; if a
  chart patch is meant to publish, bump that field even when `appVersion`
  stays unchanged.
- Add or update the corresponding versioned entry in `CHANGELOG.md`. Include the
  chart version, application image version, date, and a concise list of changes.
- When a chart change depends on new application code or CLI flags, bump the
  application image version at the same time and update `appVersion`, the
  default `image.tag`, Artifact Hub image metadata, and release notes together.
- Keep the default `image.tag` in `chart/values.yaml` aligned with
  `chart/Chart.yaml` `appVersion` and the Artifact Hub image metadata.
- Keep `artifacthub.io/changes` in `chart/Chart.yaml` aligned with the current
  chart release. It describes only the changes in that release.
- Keep the chart installation examples in `chart/README.md` synchronized with
  the current chart version.
- Verify `chart/values.schema.json` whenever `chart/` changes, and update it in
  the same change when chart values or CLI flags are added, removed, or renamed.
- Run `helm lint chart --values chart/ci/lint-values.yaml` when Helm is
  available. The CI workflow runs this command before publishing the chart.

## Default values

- Do not add environment-specific interfaces, remote addresses, or credentials
  to `chart/values.yaml`.
- Keep required deployment inputs validated by `chart/values.schema.json` and
  the Helm templates.
