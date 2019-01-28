from hashlib import sha256
from html.parser import HTMLParser

import pytest
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

from app import server

CAT_PATH = "/static/funny-pictures-cat-sound-studio.jpg"
CAT_SHA256 = "85f77812c365c4cb02c1972fcbfa4c5b00a108bf12d6d34da5a84a8218a5219b"


class ImgLinkHTMLParser(HTMLParser):
    """Parser to aid asserting the correct minima of cats on the page."""

    catCount = 0

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for attr in attrs:
                if attr[0] == "src" and attr[1] == CAT_PATH:
                    self.catCount += 1


@pytest.fixture
def parser():
    yield ImgLinkHTMLParser()


@pytest.fixture
def client():
    yield Client(server.create_app(server.config(parse=False)), BaseResponse)


def test_cat_linked_from_frontpage(client, parser):
    """Ensure there is cat linked from the front page."""
    resp = client.get("/")
    assert resp.status == "200 OK"
    parser.feed(str(resp.data))
    assert parser.catCount > 0


def test_cat_quality(client):
    """Ensure that cat is purrfect."""
    resp = client.get(CAT_PATH)
    assert resp.status == "200 OK"
    assert sha256(resp.data).hexdigest() == CAT_SHA256


def test_err(client):
    """Check if errors to happen."""
    resp = client.get("/404")
    assert resp.status == "404 NOT FOUND"
