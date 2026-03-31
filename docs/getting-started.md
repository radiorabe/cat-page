# Getting Started

RaBe Cat Landing Page is the overengineered intranet landing page for
[Radio Bern RaBe](https://www.rabe.ch). It serves configurable links over a JSON
API, renders a Jinja2 HTML template with offline support, and ships as a container
image you can drop into any OCI-compatible runtime.

## Quick Start

Pull and run the latest image:

```bash
# using docker
docker run --rm -p 8080:8080 ghcr.io/radiorabe/catpage

# or podman
podman run --rm -p 8080:8080 ghcr.io/radiorabe/catpage
```

Open [localhost:8080](http://localhost:8080) in your browser.
You will see the default landing page with a handful of example links.

## Adding Your Own Links

Pass links as semicolon-separated `name;target` pairs via the `PAGE_LINKS`
environment variable (repeat the flag for each link):

```bash
docker run --rm -p 8080:8080 \
  -e PAGE_TITLE="My Intranet" \
  -e PAGE_LINKS="Wiki;https://wiki.example.org" \
  -e PAGE_LINKS="Mail;https://mail.example.org" \
  -e PAGE_LINKS="Monitoring;https://grafana.example.org" \
  ghcr.io/radiorabe/catpage
```

## Compose Example

```yaml title="compose.yaml"
services:
  catpage:
    image: ghcr.io/radiorabe/catpage:latest
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      PAGE_TITLE: My Intranet
      PAGE_LINKS: |
        Wiki;https://wiki.example.org
        Mail;https://mail.example.org
        Grafana;https://grafana.example.org
```

Or use the provided example file as a starting point:

```bash
cp env.example .env
$EDITOR .env
podman-compose up -d
```

## Kubernetes

Install the Helm chart from the OCI registry:

```bash
helm install catpage oci://ghcr.io/radiorabe/helm/catpage --version x.y.z
```

## Next Steps

- Read the [Configuration Reference](configuration.md) for every available option.
- Set up a [Development Environment](contributing.md) to contribute or customise the page.
