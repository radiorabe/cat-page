# Agent Instructions: app/

## Purpose

This directory contains the Python application package for the RaBe Cat Landing Page.
The app is a [Quart](https://quart.palletsprojects.com/) ASGI application (pallets project)
served by [Hypercorn](https://hypercorn.readthedocs.io/) in production. It exposes four routes:

| Route | Handler | Description |
|---|---|---|
| `/` | `on_site` | Renders the main landing page (Jinja2 HTML template) |
| `/sw.js` | `on_service_worker` | Returns the service worker (Jinja2 JS template) |
| `/api` | `on_api` | Returns links as JSON (`{"version": ..., "links": [...]}`) |
| `/.env`, `/wp-login.php`, `/wp-admin` | `on_hack` | Rickrolls probe attempts |

Static assets under `app/static/` are served by Quart's built-in static file handling at `/static`.

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
- **Async handlers**: All route handlers are `async def` with no `request` parameter —
  use `quart.request` context variable if request data is needed in the future.
- **Return type**: Handler return type is `ResponseReturnValue` (from `quart.typing`), which
  covers Quart/Werkzeug responses, strings, dicts, and tuples.
- **Type annotations**: Required on all public functions and class methods. `mypy` is run as
  part of the test suite via `pytest-mypy`.
- **`Self` type**: Use `from typing import Self` for `self` parameters in class methods.
- **Linting**: `ruff` with `ruff-format`. Config in `ruff.toml` at the repository root.
- **Caching**: The `_render_template` method caches rendered templates in `SimpleCache` with
  `timeout=0` (never expires). Cache is keyed by template name. Context values come from
  config, which is fixed at server construction time.
- **Configuration**: `get_config()` uses `configargparse` with env vars prefixed `PAGE_*`.
  Config files are searched in `/etc/`, `~`, and `.` (current directory).
- **`create_app()`**: Accepts an optional `ArgparseNamespace`; when called without arguments
  it reads config from env vars / config files.
- **Server startup**: `Quart.run()` is used for both dev (`use_reloader=True`) and prod
  (`use_reloader=False`). Hypercorn is used internally by Quart and is not imported directly.

## Configuration Reference

| Flag | Env var | Default | Description |
|---|---|---|---|
| `--title` | `PAGE_TITLE` | `RaBe Intranet` | Page `<title>` |
| `--background-image` | `PAGE_BACKGROUND` | RaBe header GIF URL | CSS background image |
| `--links` | `PAGE_LINKS` | Three example links | Repeatable `Name;URL` entries |
| `--address` | `PAGE_ADDRESS` | `127.0.0.1` | Bind address |
| `--port` | `PAGE_PORT` | `8080` | Bind port |
| `--dev` / `--no-dev` | — | `False` | Use `use_reloader=True` (auto-reload on code changes) |
| `--static` / `--no-static` | — | `True` | Serve `/static` via Quart built-in static handling |

## Running Locally

```bash
poetry run catpage                       # production (Quart/Hypercorn, no auto-reload)
poetry run python -m app.server --dev    # development (Quart/Hypercorn, auto-reload)
```

## llms.txt

- [quart.palletsprojects.com](https://quart.palletsprojects.com/) – Quart async ASGI framework (pallets project)
- [jinja.palletsprojects.com](https://jinja.palletsprojects.com/) – Jinja2 templating engine
