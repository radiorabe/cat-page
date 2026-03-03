# Agent Instructions: charts/

## Purpose

This directory contains the [Helm](https://helm.sh/) chart for deploying the Cat Page to
Kubernetes. The chart is published to `oci://ghcr.io/radiorabe/helm/catpage` as part of the
release workflow.

## Directory Layout

```
charts/catpage/
  Chart.yaml          # Chart metadata (name, version, appVersion)
  values.yaml         # Default values (image, service, ingress, autoscaling, …)
  .helmignore         # Files excluded from the chart package
  templates/
    _helpers.tpl      # Named templates (fullname, labels, selectorLabels, …)
    deployment.yaml   # Kubernetes Deployment
    service.yaml      # Kubernetes Service (ClusterIP, port 8080)
    serviceaccount.yaml  # Optional ServiceAccount
    ingress.yaml      # Optional Ingress
    hpa.yaml          # Optional HorizontalPodAutoscaler
    NOTES.txt         # Post-install notes printed by Helm
    tests/
      test-connection.yaml  # Helm test: wget to the service port
```

## Key Conventions

- **Versioning**: `Chart.yaml` uses `version: 0.0.0` and `appVersion: "latest"` as
  placeholders. These are replaced during the release workflow by the actual semver tag.
- **Image**: Default image is `ghcr.io/radiorabe/catpage` with `pullPolicy: IfNotPresent`.
  Override with `--set image.tag=<version>` or via `values.yaml`.
- **Port**: The application listens on `8080`. The `service.port` default matches this.
- **Helm test**: `charts/catpage/templates/tests/test-connection.yaml` uses `wget` to check
  the service is reachable. Run with `helm test <release-name>`.
- **chart-testing**: CI uses `ct` (chart-testing) with `.github/ct.yaml` for lint and
  install testing. The `target-branch` is `main`.

## Local Testing

```bash
# Lint the chart
helm lint charts/catpage

# Render templates locally (dry-run)
helm template catpage charts/catpage

# Run chart-testing lint
ct lint --config .github/ct.yaml

# Install into a local kind cluster (requires kind and a running cluster)
ct install --config .github/ct.yaml
```

## Publishing

The chart is packaged and pushed by the `helm-chart` job in `.github/workflows/release.yaml`
when a version tag is pushed. No manual steps are required.

## llms.txt

- [helm.sh/docs](https://helm.sh/docs/) – Helm documentation
