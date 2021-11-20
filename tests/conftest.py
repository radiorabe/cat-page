from html.parser import HTMLParser

import pytest
from werkzeug.test import Client
from werkzeug.wrappers import Response

from app import server

CAT_PATH = "/static/funny-pictures-cat-sound-studio.jpg"


class CatImgLinkHTMLParser(HTMLParser):
    """Parser to aid asserting the correct minima of cats on the page."""

    catCount = 0

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for attr in attrs:
                if attr[0] == "src" and attr[1] == self.cat_path:
                    self.catCount += 1


@pytest.fixture
def cat_path():
    return CAT_PATH


@pytest.fixture
def cat_parser(cat_path=CAT_PATH):
    cilhp = CatImgLinkHTMLParser()
    cilhp.cat_path = cat_path
    yield cilhp


@pytest.fixture
def client():
    yield Client(server.create_app(server.config(parse=False)), Response)
