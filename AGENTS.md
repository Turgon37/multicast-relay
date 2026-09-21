# Repository instructions

## Release workflow

- Official Docker image releases are tag-based only: the `docker-image.yml`
  workflow runs on Git tags matching `v*`.
- `master` can still publish pre-release `rc` images for validation. Treat
  those as disposable build outputs, not as official releases.
- The Helm chart keeps an independent version stream and is published from the
  chart workflow after the chart metadata is bumped.
- When preparing a release, do not create or push Git tags from the agent.
  Instead, explain the exact shell command the user should run, for example a
  `git tag ...` and `git push origin ...` sequence.

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
- For a clean chart reset, keep the chart version stream independent from the
  application version stream. Chart bumps still require the chart metadata,
  README, changelog and release notes to stay in sync.
- Verify `chart/values.schema.json` whenever `chart/` changes, and update it in
  the same change when chart values or CLI flags are added, removed, or renamed.
- Run `helm lint chart --values chart/ci/lint-values.yaml` when Helm is
  available. The CI workflow runs this command before publishing the chart.

## Application and image changes

- When changing runtime code or Docker image construction, update the image
  release inputs together: `chart/Chart.yaml` `appVersion`, the default
  `chart/values.yaml` image tag, Artifact Hub image metadata, and any release
  notes that describe the image.
- If the change is intended for an official image release, target a Git tag and
  let CI publish the image from that tag. Do not manually publish from the
  agent.
- If the change is meant for ongoing validation on `master`, keep it on the rc
  stream so the workflows can publish `rc` images automatically.

## Default values

- Do not add environment-specific interfaces, remote addresses, or credentials
  to `chart/values.yaml`.
- Keep required deployment inputs validated by `chart/values.schema.json` and
  the Helm templates.
