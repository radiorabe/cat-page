"""Configure test environment."""

from html.parser import HTMLParser

import pytest
from werkzeug.test import Client
from werkzeug.wrappers import Response

from app import server

CAT_PATH = "/static/funny-pictures-cat-sound-studio.jpg"


class CatImgLinkHTMLParser(HTMLParser):  # pylint: disable=abstract-method
    """Parser to aid asserting the correct minima of cats on the page."""

    def __init__(self, cat_path):
        self.cat_count = 0
        self.cat_path = cat_path
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for attr in attrs:
                if attr[0] == "src" and attr[1] == self.cat_path:
                    self.cat_count += 1


@pytest.fixture(name="cat_path")
def cat_path_fixture():
    """Return path to cat."""
    return CAT_PATH


@pytest.fixture()
def cat_parser(cat_path=CAT_PATH):
    """Return parser stub."""
    return CatImgLinkHTMLParser(cat_path=cat_path)


@pytest.fixture()
def client():
    """Server for testing."""
    return Client(server.create_app(server.get_config(parse=False)), Response)
