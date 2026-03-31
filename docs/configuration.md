# Configuration

All configuration is driven by environment variables (or command-line flags).
Run `python app/server.py --help` to see the full usage message.

## Environment Variables

| Variable | Flag | Default | Description |
|---|---|---|---|
| `PAGE_TITLE` | `--title` | `RaBe Intranet` | Title shown in the browser tab and page heading |
| `PAGE_BACKGROUND` | `--background-image` | RaBe header GIF | URL of the background image |
| `PAGE_LINKS` | `--links` | three example links | Repeat for each link, formatted as `name;target` |
| `PAGE_ADDRESS` | `--address` | `127.0.0.1` | Bind address for the HTTP server |
| `PAGE_PORT` | `--port` | `8080` | Port for the HTTP server |

## Links Format

Each link is a semicolon-separated pair: `Display Name;URL`.
Pass one link per environment variable occurrence (or `--links` flag):

```bash
PAGE_LINKS="Studiomail;https://studiomail.example.org"
PAGE_LINKS="Homepage;https://www.rabe.ch"
PAGE_LINKS="Wiki;https://wiki.example.org"
```

Internal links (protocol-relative) are supported too:

```bash
PAGE_LINKS="Internal Tool;//tool.int.example.org"
```

## Config File

Settings can also be read from a config file.
The server looks for `server.conf` in the following locations (later files override
earlier ones):

1. `/etc/server.conf`
2. `~/server.conf`
3. `./server.conf`

Example `server.conf`:

```ini
title = My Intranet
links = Wiki;https://wiki.example.org
links = Mail;https://mail.example.org
```

## Additional Flags

| Flag | Default | Description |
|---|---|---|
| `--static` / `--no-static` | `--static` | Serve static assets (CSS, JS, icons) from the built-in path |
| `--dev` / `--no-dev` | `--no-dev` | Enable development mode with auto-reload |

## JSON API

The `/api` endpoint returns all configured links as JSON:

```json
{
  "version": "0.7.0",
  "links": [
    {"name": "Wiki", "target": "https://wiki.example.org"},
    {"name": "Mail", "target": "https://mail.example.org"}
  ]
}
```

This is useful for building dashboards, browser extensions, or any tool that
needs to consume the link list programmatically.
