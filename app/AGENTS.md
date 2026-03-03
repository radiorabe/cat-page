# Agent Instructions: app/

## Purpose

This directory contains the Python application package for the RaBe Cat Landing Page.
The app is a [Werkzeug](https://werkzeug.palletsprojects.com/) WSGI application served by
[CherryPy](https://cherrypy.dev/) in production. It exposes four routes:

| Route | Handler | Description |
|---|---|---|
| `/` | `on_site` | Renders the main landing page (Jinja2 HTML template) |
| `/sw.js` | `on_service_worker` | Returns the service worker (Jinja2 JS template) |
| `/api` | `on_api` | Returns links as JSON (`{"version": ..., "links": [...]}`) |
| `/.env`, `/wp-login.php`, `/wp-admin` | `on_hack` | Rickrolls probe attempts |

Static assets under `app/static/` are served by `SharedDataMiddleware` at `/static`.

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
- **Type annotations**: Required on all public functions and class methods. `mypy` is run as
  part of the test suite via `pytest-mypy`.
- **`Self` type**: Use `from typing import Self` for `self` parameters in class methods.
- **Linting**: `ruff` with `ruff-format`. Config in `ruff.toml` at the repository root.
- **Caching**: The `render_template` method caches rendered templates in `SimpleCache` with
  `timeout=0` (never expires). Cache is keyed by template name.
- **Configuration**: `get_config()` uses `configargparse` with env vars prefixed `PAGE_*`.
  Config files are searched in `/etc/`, `~`, and `.` (current directory).

## Configuration Reference

| Flag | Env var | Default | Description |
|---|---|---|---|
| `--title` | `PAGE_TITLE` | `RaBe Intranet` | Page `<title>` |
| `--background-image` | `PAGE_BACKGROUND` | RaBe header GIF URL | CSS background image |
| `--links` | `PAGE_LINKS` | Three example links | Repeatable `Name;URL` entries |
| `--address` | `PAGE_ADDRESS` | `127.0.0.1` | Bind address |
| `--port` | `PAGE_PORT` | `8080` | Bind port |
| `--thread-pool` | `PAGE_THREADPOOL` | `30` | CherryPy thread pool size |
| `--dev` / `--no-dev` | — | `False` | Use Werkzeug dev server instead of CherryPy |
| `--static` / `--no-static` | — | `True` | Serve `/static` via `SharedDataMiddleware` |

## Running Locally

```bash
poetry run catpage                       # production (CherryPy)
poetry run python -m app.server --dev    # development (Werkzeug, auto-reload)
```

## llms.txt

- [werkzeug.palletsprojects.com](https://werkzeug.palletsprojects.com/) – WSGI toolkit (routing, request/response, test client, static middleware)
- [jinja.palletsprojects.com](https://jinja.palletsprojects.com/) – Jinja2 templating engine
- [cherrypy.dev](https://cherrypy.dev/) – CherryPy production WSGI server
