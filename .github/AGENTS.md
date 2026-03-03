# Agent Instructions: .github/

## Purpose

This directory contains all GitHub-specific configuration for the `radiorabe/cat-page`
repository: CI/CD workflows, Dependabot configuration, and Helm chart testing config.

## Directory Layout

```
.github/
  workflows/
    main.yaml             # PR checks: pre-commit, Python tests, Helm chart test
    release.yaml          # Release: container image, MkDocs docs, Helm chart push
    schedule.yaml         # Scheduled Trivy security scan
    semantic-release.yaml # Automated releases via go-semantic-release
  dependabot.yml          # Automated dependency updates (Docker, pip, GitHub Actions)
  ct.yaml                 # chart-testing configuration
  FUNDING.yml             # GitHub Sponsors configuration
```

## Workflow Conventions

All workflows in this repository follow the
[radiorabe/actions](https://radiorabe.github.io/actions/) security baseline:

1. **`permissions: {}`** at the top of every workflow file – denies all token permissions
   as a zero-trust starting point.
2. **Per-job `permissions:`** – grant only the minimum permissions each job requires, based on
   the [permissions reference](https://radiorabe.github.io/actions/permissions/).
3. **Reusable workflows** – most jobs call `radiorabe/actions/.github/workflows/<name>.yaml@vX.Y.Z`.
   Dependabot keeps these version pins up to date automatically.
4. **Pin all third-party actions** to a released version tag (e.g. `@v4`). Do not use commit SHAs.

### Permissions Reference (this repo)

| Workflow | Job | Required permissions |
|---|---|---|
| `main.yaml` | `pre-commit` | `contents: read` |
| `main.yaml` | `python-poetry` | `contents: read` |
| `main.yaml` | `helm-chart` | `contents: read` |
| `release.yaml` | `release-container` | `contents: read`, `packages: write`, `security-events: write`, `id-token: write` |
| `release.yaml` | `release-mkdocs` | `contents: write` |
| `release.yaml` | `helm-chart` | `contents: read`, `packages: write` |
| `schedule.yaml` | `schedule-trivy` | `packages: write`, `security-events: write`, `id-token: write` |
| `semantic-release.yaml` | `semantic-release` | `contents: read` |

## Dependabot

`dependabot.yml` keeps three ecosystems up-to-date with daily checks:

- **`docker`** – base images in `Dockerfile`
- **`github-actions`** – action version pins in `.github/workflows/`
- **`pip`** – Python dependencies in `pyproject.toml` / `poetry.lock`

All Dependabot PRs use `chore:` or `chore(ci):` commit prefixes and are grouped so that
related updates land in a single PR.

## llms.txt

- [radiorabe.github.io/actions/llms.txt](https://radiorabe.github.io/actions/llms.txt) – RaBe reusable workflows reference
- [docs.github.com/llms.txt](https://docs.github.com/llms.txt) – GitHub Actions platform docs
