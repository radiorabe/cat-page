"""Server that hosts our landing page thing with a cat."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:  # pragma: no cover
    from argparse import Namespace as ArgparseNamespace

    from starlette.requests import Request

import uvicorn
from cachelib.simple import SimpleCache
from configargparse import ArgumentParser  # type: ignore[import-untyped]
from jinja2 import Environment, FileSystemLoader
from starlette.applications import Starlette
from starlette.responses import JSONResponse, RedirectResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

__version__ = "0.7.0"

logger = logging.getLogger("catpage")


def get_config(*, parse: bool = True) -> ArgparseNamespace:
    """Get ConfigargParse based configuration.

    The config file in /etc gets overriden by the one in $HOME which gets
    overriden by the one in the current directory. Everything can also be
    set from environment variables.
    """
    default_config_file = Path(__file__).name.replace(".py", ".conf")
    default_config_files = [
        "/etc/" + default_config_file,
        Path("~").expanduser() / default_config_file,
        default_config_file,
    ]
    parser = ArgumentParser(
        default_config_files=default_config_files,
        description="RaBe Intranet Landing Page",
    )
    parser.add_argument("--title", env_var="PAGE_TITLE", default="RaBe Intranet")
    parser.add_argument(
        "--background-image",
        env_var="PAGE_BACKGROUND",
        default="https://rabe.ch/wp-content/uploads/2016/07/Header.gif",
    )
    parser.add_argument("--links", env_var="PAGE_LINKS", action="append", default=[])
    parser.add_argument("--address", env_var="PAGE_ADDRESS", default="127.0.0.1")
    parser.add_argument("--port", env_var="PAGE_PORT", default=8080)
    parser.add_argument("--thread-pool", env_var="PAGE_THREADPOOL", default=30)

    def add_bool_arg(
        parser: ArgumentParser,
        name: str,
        *,
        default: bool = False,
    ) -> None:
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument("--" + name, dest=name, action="store_true")
        group.add_argument("--no-" + name, dest=name, action="store_false")
        parser.set_defaults(**{name: default})

    add_bool_arg(parser, "static", default=True)
    add_bool_arg(parser, "dev")

    args = parser.parse_args() if parse else parser.parse_args([])
    logger.info(parser.format_values())

    if not args.links:
        args.links = [
            "Studiomail;//studiomail.int.example.org",
            "Homepage;https://www.rabe.ch",
            "Intranet;//wiki.int.example.org/",
        ]

    if args.links:

        def link_split(link: str) -> dict[str, str]:
            split = link.split(";")
            return {"name": split[0], "target": split[1]}

        args.links = list(map(link_split, args.links))
    if args.port:
        args.port = int(args.port)

    return args


class Server:
    """Main server renders the landing page and serves the API."""

    def __init__(self: Self, config: ArgparseNamespace) -> None:
        """Initialize server with cache and templates."""
        self.page_title = config.title
        self.page_background_image = config.background_image
        self.links = config.links

        self.cache = SimpleCache()

        template_path = Path(__file__).parent / "templates"
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=True,
        )

    async def on_site(self: Self, _: Request) -> Response:
        """Return main / page."""
        return self._render_template(
            "index.html",
            title=self.page_title,
            background_url=self.page_background_image,
            links=self.links,
            version=__version__,
        )

    async def on_service_worker(self: Self, _: Request) -> Response:
        """Return a service worker for SPA reasons."""
        return self._render_template(
            "sw.js",
            media_type="application/javascript",
        )

    async def on_api(self: Self, _: Request) -> Response:
        """Return links as JSON."""
        return JSONResponse({"version": __version__, "links": self.links})

    async def on_hack(self: Self, _: Request) -> Response:
        """Rickroll people trying to break in."""
        return RedirectResponse(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            status_code=302,
        )

    def _render_template(
        self: Self,
        template_name: str,
        media_type: str = "text/html",
        **context: Any,  # noqa: ANN401
    ) -> Response:
        """Render template to cache and keep in cache forever.

        The cache is keyed by template name. Context values come from config,
        which is fixed at server construction time, so the same template always
        renders with the same context within a server instance.
        """
        if not self.cache.has(template_name):
            tpl = self.jinja_env.get_template(template_name)
            self.cache.set(template_name, tpl.render(**context), timeout=0)

        return Response(self.cache.get(template_name), media_type=media_type)


def create_app(config: ArgparseNamespace | None = None) -> Starlette:
    """Create the ASGI app."""
    if config is None:
        config = get_config(parse=False)
    srv = Server(config)
    routes: list[Route | Mount] = [
        Route("/", srv.on_site),
        Route("/sw.js", srv.on_service_worker),
        Route("/api", srv.on_api),
        Route("/.env", srv.on_hack),
        Route("/wp-login.php", srv.on_hack),
        Route("/wp-admin", srv.on_hack),
    ]
    if config.static:
        routes.append(
            Mount("/static", StaticFiles(directory=Path(__file__).parent / "static")),
        )
    return Starlette(routes=routes)


def run_devserver(config: ArgparseNamespace) -> None:  # pragma: no cover
    """Run a uvicorn dev server with auto-reload."""
    logger.info("Starting development server")
    uvicorn.run(
        "app.server:create_app",
        factory=True,
        host=config.address,
        port=config.port,
        reload=True,
    )


def run_webserver(config: ArgparseNamespace) -> None:  # pragma: no cover
    """Run the production uvicorn server."""
    logger.info("Starting production server")
    uvicorn.run(
        "app.server:create_app",
        factory=True,
        host=config.address,
        port=config.port,
        workers=config.thread_pool,
    )


def main() -> None:  # pragma: no cover
    """Start dev or prod server."""
    logger.info("Starting cat-page server version %s", __version__)
    cfg = get_config()
    if cfg.dev:
        run_devserver(cfg)
    else:
        run_webserver(cfg)


if __name__ == "__main__":  # pragma: no cover
    main()
