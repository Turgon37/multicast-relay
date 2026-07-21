# Repository instructions

## Helm chart changes

- Treat every change under `chart/` that affects the packaged chart as a chart
  release change.
- Increment `version` in `chart/Chart.yaml` before publishing a modified chart.
- Add or update the corresponding versioned entry in `CHANGELOG.md`. Include the
  chart version, application image version, date, and a concise list of changes.
- Keep `artifacthub.io/changes` in `chart/Chart.yaml` aligned with the current
  chart release. It describes only the changes in that release.
- Keep the chart installation examples in `chart/README.md` synchronized with
  the current chart version.
- Run `helm lint chart --values chart/ci/lint-values.yaml` when Helm is
  available. The CI workflow runs this command before publishing the chart.

## Default values

- Do not add environment-specific interfaces, remote addresses, or credentials
  to `chart/values.yaml`.
- Keep required deployment inputs validated by `chart/values.schema.json` and
  the Helm templates.
