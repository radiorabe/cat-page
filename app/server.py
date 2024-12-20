"""Server that hosts our langing page thing with a cat."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:  # pragma: no cover
    from argparse import Namespace as ArgparseNamespace
    from collections.abc import Iterable
    from wsgiref.types import StartResponse, WSGIEnvironment

import cherrypy  # type: ignore[import-untyped]
from cachelib.simple import SimpleCache
from configargparse import ArgumentParser  # type: ignore[import-untyped]
from jinja2 import Environment, FileSystemLoader
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response

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
    """Main server servers static assets and renderds main page with links."""

    DEFAULT_CACHE_TIMEOUT = 60 * 60 * 24 * 30

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
        self.url_map = Map(
            [
                Rule("/", endpoint="site"),
                Rule("/sw.js", endpoint="service_worker"),
                Rule("/api", endpoint="api"),
                Rule("/.env", endpoint="hack"),
                Rule("/wp-login.php", endpoint="hack"),
                Rule("/wp-admin", endpoint="hack"),
            ],
        )

    def dispatch_request(self: Self, request: Request) -> Response | HTTPException:
        """Dispatch requests to handlers."""
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()  # pylint: disable=unpacking-non-sequence
            return getattr(self, "on_" + endpoint)(request, **values)
        except HTTPException as ex:
            return ex

    def on_site(self: Self, _: Request) -> Response:
        """Return main / page."""
        return self.render_template(
            "index.html",
            title=self.page_title,
            background_url=self.page_background_image,
            links=self.links,
            version=__version__,
        )

    def on_service_worker(self: Self, _: Request) -> Response:
        """Return a service worker for SPA reasons."""
        return self.render_template(
            "sw.js",
            mimetype="application/javascript",
            background_url=self.page_background_image,
        )

    def on_api(self: Self, _: Request) -> Response:
        """Return links as JSON request."""
        return Response(
            json.dumps({"version": __version__, "links": self.links}),
            mimetype="application/json",
        )

    def on_hack(self: Self, _: Request) -> Response:
        """Rickroll people trying to break in."""
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    def wsgi_app(
        self: Self,
        environ: WSGIEnvironment,
        start_response: StartResponse,
    ) -> Iterable[bytes]:
        """Return a wsgi app."""
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(
        self: Self,
        environ: WSGIEnvironment,
        start_response: StartResponse,
    ) -> Iterable[bytes]:
        """Forward calls to wsgi_app."""
        return self.wsgi_app(environ, start_response)

    def render_template(
        self: Self,
        template_name: str,
        mimetype: str = "text/html",
        **context: Any,  # noqa: ANN401
    ) -> Response:
        """Render template to cache and keep in cache forver."""
        if not self.cache.has(template_name):
            tpl = self.jinja_env.get_template(template_name)
            self.cache.set(template_name, tpl.render(context), timeout=0)

        return Response(self.cache.get(template_name), mimetype=mimetype)


def create_app(config: ArgparseNamespace) -> Server:
    """Create the app server."""
    app = Server(config)
    if config.static:
        app.wsgi_app = SharedDataMiddleware(  # type: ignore[method-assign]
            app.wsgi_app,
            {"/static": str(Path(__file__).parent / "static")},  # type: ignore[arg-type]
            cache_timeout=Server.DEFAULT_CACHE_TIMEOUT,
        )
    return app


def run_devserver(
    app: Server,
    config: ArgparseNamespace,
) -> None:  # pragma: no cover
    """Run a simple werkzeug devserver."""
    logger.info("Starting development server")

    run_simple(config.address, config.port, app, use_debugger=True, use_reloader=True)  # type: ignore[arg-type]


def run_webserver(
    app: Server,
    config: ArgparseNamespace,
) -> None:  # pragma: no cover
    """Run the production cherrypy server."""
    logger.info("Starting production server")

    cherrypy.tree.graft(app, "/")
    cherrypy.server.unsubscribe()

    server = cherrypy._cpserver.Server()  # noqa: SLF001

    server.socket_host = config.address
    server.socket_port = config.port
    server.thread_pool = config.thread_pool

    server.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()


def main() -> None:  # pragma: no cover
    """Start dev or prod server."""
    logger.info("Starting cat-page server version %s", __version__)
    cfg = get_config()
    app = create_app(cfg)
    if cfg.dev:
        run_devserver(app, cfg)
    else:
        run_webserver(app, cfg)


if __name__ == "__main__":  # pragma: no cover
    main()
