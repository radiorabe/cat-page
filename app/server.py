import json
import logging
import os
from os.path import basename, expanduser

from cachelib.simple import SimpleCache
from configargparse import ArgumentParser
from jinja2 import Environment, FileSystemLoader
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response

__version__ = "0.6.0"

logger = logging.getLogger("catpage")


def config(parse=True):
    """Get ConfigargParse based configuration.

    The config file in /etc gets overriden by the one in $HOME which gets
    overriden by the one in the current directory. Everything can also be
    set from environment variables.
    """
    default_config_file = basename(__file__).replace(".py", ".conf")
    default_config_files = [
        "/etc/" + default_config_file,
        expanduser("~") + "/" + default_config_file,
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
    parser.add_argument("--address", env_var="PAGE_ADDRESS", default="0.0.0.0")
    parser.add_argument("--port", env_var="PAGE_PORT", default=5000)
    parser.add_argument("--thread-pool", env_var="PAGE_THREADPOOL", default=30)

    def add_bool_arg(parser, name, default=False):
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument("--" + name, dest=name, action="store_true")
        group.add_argument("--no-" + name, dest=name, action="store_false")
        parser.set_defaults(**{name: default})

    add_bool_arg(parser, "static", default=True)
    add_bool_arg(parser, "dev")

    if parse:  # pragma: no cover
        args = parser.parse_args()
    else:
        args = parser.parse_args([])
    logger.info(parser.format_values())

    if not args.links:
        args.links = [
            "Studiomail;//studiomail.int.example.org",
            "Homepage;https://www.rabe.ch",
            "Intranet;//wiki.int.example.org/",
        ]

    if args.links:

        def link_split(l):
            s = l.split(";")
            return {"name": s[0], "target": s[1]}

        args.links = list(map(link_split, args.links))
    if args.port:
        args.port = int(args.port)

    return args


class Server(object):
    """Main server servers static assets and renderds main page with links."""

    DEFAULT_CACHE_TIMEOUT = 60 * 60 * 24 * 30

    def __init__(self, config):
        self.page_title = config.title
        self.page_background_image = config.background_image
        self.links = config.links

        self.cache = SimpleCache()

        template_path = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_path), autoescape=True
        )
        self.url_map = Map(
            [
                Rule("/", endpoint="site"),
                Rule("/sw.js", endpoint="service_worker"),
                Rule("/api", endpoint="api"),
            ]
        )

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, "on_" + endpoint)(request, **values)
        except HTTPException as e:
            return e

    def on_site(self, request):
        """Return main / page."""
        return self.render_template(
            "index.html",
            title=self.page_title,
            background_url=self.page_background_image,
            links=self.links,
            version=__version__,
        )

    def on_service_worker(self, request):
        return self.render_template(
            "sw.js",
            mimetype="application/javascript",
            background_url=self.page_background_image,
        )

    def on_api(self, request):
        """Return links as JSON request."""
        return Response(
            json.dumps({"version": __version__, "links": self.links}),
            mimetype="application/json",
        )

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def render_template(self, template_name, mimetype="text/html", **context):
        """Render template to cache and keep in cache forver."""
        if not self.cache.has(template_name):
            t = self.jinja_env.get_template(template_name)
            self.cache.set(template_name, t.render(context), timeout=0)

        return Response(self.cache.get(template_name), mimetype=mimetype)


def create_app(config):
    app = Server(config)
    if config.static:
        app.wsgi_app = SharedDataMiddleware(
            app.wsgi_app,
            {"/static": os.path.join(os.path.dirname(__file__), "static")},
            cache_timeout=Server.DEFAULT_CACHE_TIMEOUT,
        )
    return app


def run_devserver(app, config):  # pragma: no cover
    from werkzeug.serving import run_simple

    logger.info("Starting development server")

    run_simple(config.address, config.port, app, use_debugger=True, use_reloader=True)


def run_webserver(app, config):  # pragma: no cover
    import cherrypy

    logger.info("Starting production server")

    cherrypy.tree.graft(app, "/")
    cherrypy.server.unsubscribe()

    server = cherrypy._cpserver.Server()

    server.socket_host = config.address
    server.socket_port = config.port
    server.thread_pool = config.thread_pool

    server.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":  # pragma: no cover
    logger.info("Starting cat-page server version {0}".format(__version__))
    config = config()
    app = create_app(config)
    if config.dev:
        run_devserver(app, config)
    else:
        run_webserver(app, config)
