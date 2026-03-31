# Agent Instructions: tests/

## Purpose

This directory contains the [pytest](https://docs.pytest.org/) test suite for the
`app/` package. **100% branch coverage is required** and enforced by CI (`--cov-fail-under=100`).

## Test Files

| File | What it tests |
|---|---|
| `conftest.py` | Shared fixtures: `client`, `cat_parser`, `cat_path` |
| `test_api.py` | `/api` endpoint returns `200 OK` |
| `test_cat.py` | Cat image linked from front page; cat SHA-256 integrity; 404 handling |
| `test_rick.py` | Hack-probe endpoints redirect to the Rick Astley video |
| `test_service_worker.py` | `/sw.js` returns `200 OK` |

## Key Conventions

- **Fixtures** (`conftest.py`): Use `quart.typing.TestClientProtocol` via `app.test_client()`
  against a `Quart` app created with `server.create_app(server.get_config(parse=False))`.
  The fixture is `async` (requires `pytest-asyncio` with `asyncio_mode = "auto"`).
- **All tests are async**: Test functions are `async def` and use `await client.get(...)`.
  Response body is accessed via `await resp.get_data()` (bytes) or
  `await resp.get_data(as_text=True)` (string).
- **Coverage**: Every new branch in `app/server.py` requires a corresponding test. Check with
  `poetry run pytest --cov=app --cov-report=term-missing`.
- **Type checking**: `pytest-mypy` runs mypy as part of the test collection phase.
- **Linting**: `pytest-ruff` runs ruff checks as part of test collection.
- **Random order**: `pytest-random-order` randomises test execution order to catch order
  dependencies. Re-run with `--randomly-seed=last` to reproduce a specific order.

## Running Tests

```bash
# Full suite (coverage + mypy + ruff)
poetry run pytest

# Quick run without coverage enforcement
poetry run pytest --no-cov

# Show coverage gaps
poetry run pytest --cov=app --cov-report=term-missing

# Reproduce a specific random order
poetry run pytest --randomly-seed=<seed>
```

## llms.txt

- [docs.pytest.org](https://docs.pytest.org/) – pytest documentation
