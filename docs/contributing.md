# Contributing

Thank you for your interest in contributing to RaBe Cat Landing Page!
This guide explains how to report issues, propose changes, and submit pull requests.

## Reporting Issues

Open an issue on [GitHub](https://github.com/radiorabe/cat-page/issues) if you:

- Find a bug or unexpected behaviour
- Have a feature request or improvement idea
- Encounter documentation that is unclear or incorrect

Please include as much context as possible: the version you are running, relevant
environment variable values (redact secrets!), and the steps needed to reproduce the issue.

## Development Setup

### Prerequisites

- Python 3.12 or later
- [Poetry](https://python-poetry.org/) (installed globally or via `pipx`)
- Node.js (for commitizen — optional but recommended)

### Setup

```bash
# Clone the repository
git clone https://github.com/radiorabe/cat-page.git
cd cat-page

# Create a virtual environment and install all dependencies
python -m venv venv
. ./venv/bin/activate
pipx install poetry
poetry install
```

### Running the Development Server

```bash
poetry run python -m app.server --dev
```

Open [localhost:8080](http://localhost:8080). The server auto-reloads on code changes.

### Running Tests

The full test suite includes unit and integration tests, type checking (mypy), linting
(ruff), and a 100 % coverage gate:

```bash
poetry run pytest
```

To run quickly without the coverage gate:

```bash
poetry run pytest --no-cov
```

### What the Test Suite Checks

| Check | Tool | Config |
|---|---|---|
| Tests + coverage (100 % required) | pytest + pytest-cov | `pyproject.toml` |
| Type checking | mypy (strict) | `pyproject.toml` |
| Linting + formatting | ruff | `ruff.toml` |

### Linting and Formatting

```bash
# Check for lint errors
ruff check

# Auto-fix lint errors where possible
ruff check --fix

# Format code
ruff format
```

### Pre-commit Hooks

Install the pre-commit hooks to automatically lint and format on every commit:

```bash
pip install pre-commit
pre-commit install
```

## Pull Requests

1. **Fork** the repository and create a feature branch from `main`.
2. Make your changes following the coding conventions below.
3. Add or update tests so that **coverage remains at 100 %**.
4. Run the full test suite before opening a PR:
   ```bash
   poetry run pytest
   ```
5. Open a pull request against `main`. Use a
   [Conventional Commit](https://www.conventionalcommits.org/) subject line — this drives
   automated releases.

Please keep individual contributions self-contained in a single squashed commit so
maintainers can use **Squash and merge**.

## Coding Conventions

- **Ruff** is the linter and formatter. Run `ruff check --fix` and `ruff format` before committing.
- **Full type annotations** everywhere. mypy is run in strict mode via pytest-mypy.
- **100 % test coverage** is enforced by CI. Every new code path needs a test.
- Configuration is parsed by `configargparse`; env vars use the `PAGE_*` prefix.

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>
```

| Type | Effect |
|---|---|
| `fix:` | PATCH release |
| `feat:` | MINOR release |
| `BREAKING CHANGE:` footer | MAJOR release |
| `chore:`, `docs:`, `refactor:`, `ci:` | No release |

Use `git cz` (commitizen) to help format messages:

```bash
npm install -g commitizen cz-conventional-changelog
```

## CI/CD

The GitHub Actions workflows are based on
[RaBe shared actions](https://radiorabe.github.io/actions/):

| Workflow | Trigger | Purpose |
|---|---|---|
| `test.yaml` | Pull request | Runs pytest (includes mypy and ruff) |
| `release.yaml` | Push to `main` / tags | Builds and publishes the container image |
| `release-mkdocs` | Push to `main` | Builds and deploys this documentation site |
| `semantic-release.yaml` | Push to `main` | Creates GitHub releases from conventional commits |

## Documentation

Documentation lives in `docs/` and is built with
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/). To preview locally:

```bash
pip install mkdocs-material mkdocs-section-index mkdocs-autorefs
mkdocs serve
```

Open `http://127.0.0.1:8000`. The site hot-reloads as you edit the Markdown files.

When adding new pages, register them in the `nav:` section of `mkdocs.yaml`.

## License

By contributing you agree that your contributions will be licensed under the
[GNU Affero General Public License v3](https://www.gnu.org/licenses/agpl-3.0.html).
