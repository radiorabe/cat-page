# Agent Instructions: radiorabe/cat-page

## Repository Purpose

This repository contains the **RaBe Cat Landing Page** – an overengineered intranet landing
page for [Radio Bern RaBe](https://www.rabe.ch). It serves configurable links over a JSON API,
renders a Jinja2 HTML template, and ships a service worker for offline support. The application
is a [Quart](https://quart.palletsprojects.com/) ASGI app that uses `Quart.run()` backed by
Hypercorn for both development (with auto-reload) and production.

The documentation is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
and published to GitHub Pages as part of the release workflow.

## Repository Structure

```
app/                    # Python application package
  server.py             # Entry point: ASGI app, config, routes
  static/               # Static assets served under /static
  templates/            # Jinja2 HTML/JS templates (index.html, sw.js)
tests/                  # pytest test suite (100% coverage required)
docs/                   # MkDocs source for the documentation site
  css/style.css         # Custom theme overrides
  gen_ref_pages.py      # Auto-generates index.md from README.md
charts/catpage/         # Helm chart for Kubernetes deployment
.github/workflows/      # GitHub Actions CI/CD workflows
Dockerfile              # Multi-stage container build
pyproject.toml          # Poetry project metadata and dependencies
mkdocs.yaml             # MkDocs configuration
catalog-info.yaml       # Backstage component descriptor
```

## Conventions

### Python (`app/`)

- All source lives in the `app/` package. Entry point is `app.server:main`.
- Use type annotations throughout. `mypy` is enforced by CI via `pytest-mypy`.
- Lint and format with `ruff` (config in `ruff.toml`). Pre-commit hooks run `ruff` and
  `ruff-format` on every commit.
- 100% test coverage is enforced by `pytest-cov`. Every new code path needs a test.
- Configuration is parsed by `configargparse`; env vars use `PAGE_*` prefix.

### Commits and Versioning

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` – new feature → **minor** version bump
- `fix:` – bug fix → **patch** bump
- `docs:`, `ci:`, `chore:` – no release
- `BREAKING CHANGE:` footer → **major** bump

Use `git cz` (commitizen) to help format messages. Releases are automated by
`go-semantic-release` on push to `main`.

### CI/CD (`.github/workflows/`)

All workflows use `permissions: {}` at the top level with explicit per-job grants. See
`.github/AGENTS.md` for details.

## Building and Running

```bash
# Install dependencies
poetry install

# Run development server (auto-reload)
poetry run python -m app.server --dev

# Run production server (CherryPy)
poetry run catpage

# Build container image
docker build -t ghcr.io/radiorabe/catpage:latest .

# Run container
docker run --rm -p 8080:8080 ghcr.io/radiorabe/catpage:latest
```

## Testing

```bash
# Run full test suite (coverage + mypy + ruff)
poetry run pytest

# Run quickly without coverage enforcement
poetry run pytest --no-cov
```

Tests live in `tests/`. All tests use `werkzeug.test.Client` against a live `Server` instance.
See `tests/AGENTS.md` for testing conventions.

## Documentation

```bash
pip install mkdocs-material mkdocs-section-index mkdocs-llmstxt
mkdocs serve
```

See `docs/AGENTS.md` for documentation conventions.

## Helm Chart

```bash
helm install catpage oci://ghcr.io/radiorabe/helm/catpage --version x.y.z
```

See `charts/AGENTS.md` for chart conventions.

## llms.txt

- [docs.github.com/llms.txt](https://docs.github.com/llms.txt) – GitHub Actions and the GitHub platform
- [radiorabe.github.io/actions/llms.txt](https://radiorabe.github.io/actions/llms.txt) – RaBe reusable workflows

Tool docs:

- [quart.palletsprojects.com](https://quart.palletsprojects.com/) – Quart async ASGI framework (pallets project)
- [jinja.palletsprojects.com](https://jinja.palletsprojects.com/) – Jinja2 templating
- [python-poetry.org/docs](https://python-poetry.org/docs/) – Poetry package manager
- [docs.pytest.org](https://docs.pytest.org/) – pytest test framework
- [squidfunk.github.io/mkdocs-material](https://squidfunk.github.io/mkdocs-material/) – MkDocs Material theme
- [helm.sh/docs](https://helm.sh/docs/) – Helm package manager for Kubernetes
