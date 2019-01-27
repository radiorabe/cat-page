import logging
import os
from os.path import basename, expanduser

from configargparse import ArgumentParser
from jinja2 import Environment, FileSystemLoader
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware

logger = logging.getLogger("catpage")


def config():
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
    parser.add_argument(
        "--links",
        env_var="PAGE_LINKS",
        action="append",
        default=[]
    )
    parser.add_argument("--address", env_var="PAGE_ADDRESS", default="0.0.0.0")
    parser.add_argument("--port", env_var="PAGE_PORT", default=5000)
    parser.add_argument("--thread-pool", env_var="PAGE_THREADPOOL", default=30)
    parser.add_argument("--dev", env_var="PAGE_DEVSERVER", default=False)

    args = parser.parse_args()
    logger.error(parser.format_values())

    if args.links == []:
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

    def __init__(self, config):
        self.page_title = config.title
        self.page_background_image = config.background_image
        self.links = config.links

        template_path = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_path), autoescape=True
        )
        self.url_map = Map([Rule("/", endpoint="site")])

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, "on_" + endpoint)(request, **values)
        except HTTPException as e:
            return e

    def on_site(self, request):
        return self.render_template(
            "index.html",
            title=self.page_title,
            background_url=self.page_background_image,
            links=self.links,
        )

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype="text/html")


def create_app(config, with_static=True):
    app = Server(config)
    if with_static:
        app.wsgi_app = SharedDataMiddleware(
            app.wsgi_app, {"/static": os.path.join(os.path.dirname(__file__), "static")}
        )
    return app


def run_devserver(app, config):
    from werkzeug.serving import run_simple

    logger.info("Starting development server")

    run_simple(config.address, config.port, app, use_debugger=True, use_reloader=True)


def run_webserver(app, config):
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


if __name__ == "__main__":
    config = config()
    app = create_app(config)
    if config.dev:
        run_devserver(app, config)
    else:
        run_webserver(app, config)
