# Agent Instructions: app/

## Purpose

This directory contains the Python application package for the RaBe Cat Landing Page.
The app is a [Starlette](https://www.starlette.io/) ASGI application served by
[uvicorn](https://www.uvicorn.org/) in production. It exposes four routes:

| Route | Handler | Description |
|---|---|---|
| `/` | `on_site` | Renders the main landing page (Jinja2 HTML template) |
| `/sw.js` | `on_service_worker` | Returns the service worker (Jinja2 JS template) |
| `/api` | `on_api` | Returns links as JSON (`{"version": ..., "links": [...]}`) |
| `/.env`, `/wp-login.php`, `/wp-admin` | `on_hack` | Rickrolls probe attempts |

Static assets under `app/static/` are served by Starlette's `StaticFiles` at `/static`.

## Directory Layout

```
app/
  __init__.py       # Empty package marker
  py.typed          # PEP 561 marker (enables mypy type checking)
  server.py         # All application logic: config, Server class, entry point
  static/
    funny-pictures-cat-sound-studio.jpg  # The cat
    manifest.json   # Web App Manifest (PWA)
  templates/
    index.html      # Main page Jinja2 template
    sw.js           # Service worker Jinja2 template
```

## Key Conventions

- **Single-file architecture**: All logic lives in `server.py`. Do not split into multiple
  modules unless the file grows substantially.
- **Async handlers**: All route handlers are `async def`. Keep them non-blocking; offload
  any CPU-heavy work to `anyio.to_thread.run_sync()` if needed.
- **Type annotations**: Required on all public functions and class methods. `mypy` is run as
  part of the test suite via `pytest-mypy`.
- **`Self` type**: Use `from typing import Self` for `self` parameters in class methods.
- **Linting**: `ruff` with `ruff-format`. Config in `ruff.toml` at the repository root.
- **Caching**: The `_render_template` method caches rendered templates in `SimpleCache` with
  `timeout=0` (never expires). Cache is keyed by template name. `SimpleCache` is
  in-memory and does no I/O, so it is safe to use from async handlers without `await`.
- **Configuration**: `get_config()` uses `configargparse` with env vars prefixed `PAGE_*`.
  Config files are searched in `/etc/`, `~`, and `.` (current directory).
- **`create_app()`**: Accepts an optional `ArgparseNamespace`; when called without arguments
  (e.g. by uvicorn's `--factory` mode) it reads config from env vars / config files.

## Configuration Reference

| Flag | Env var | Default | Description |
|---|---|---|---|
| `--title` | `PAGE_TITLE` | `RaBe Intranet` | Page `<title>` |
| `--background-image` | `PAGE_BACKGROUND` | RaBe header GIF URL | CSS background image |
| `--links` | `PAGE_LINKS` | Three example links | Repeatable `Name;URL` entries |
| `--address` | `PAGE_ADDRESS` | `127.0.0.1` | Bind address |
| `--port` | `PAGE_PORT` | `8080` | Bind port |
| `--thread-pool` | `PAGE_THREADPOOL` | `30` | Number of uvicorn worker processes |
| `--dev` / `--no-dev` | — | `False` | Use uvicorn with `--reload` instead of multi-worker |
| `--static` / `--no-static` | — | `True` | Mount `/static` via Starlette `StaticFiles` |

## Running Locally

```bash
poetry run catpage                       # production (uvicorn, multi-worker)
poetry run python -m app.server --dev    # development (uvicorn, auto-reload)
```

## llms.txt

- [starlette.io](https://www.starlette.io/) – Starlette ASGI toolkit (routing, request/response, static files)
- [uvicorn.org](https://www.uvicorn.org/) – uvicorn ASGI server
- [jinja.palletsprojects.com](https://jinja.palletsprojects.com/) – Jinja2 templating engine
