"""Configure test environment."""

from collections.abc import AsyncGenerator
from html.parser import HTMLParser

import pytest
from quart.typing import TestClientProtocol

from app import server

CAT_PATH = "/static/funny-pictures-cat-sound-studio.jpg"


class CatImgLinkHTMLParser(HTMLParser):
    """Parser to aid asserting the correct minima of cats on the page."""

    def __init__(self, cat_path: str) -> None:
        """Initialize parser with cat path."""
        self.cat_count = 0
        self.cat_path = cat_path
        super().__init__()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Count cat img tags."""
        if tag == "img":
            for attr in attrs:
                if attr[0] == "src" and attr[1] == self.cat_path:
                    self.cat_count += 1


@pytest.fixture(name="cat_path")
def cat_path_fixture() -> str:
    """Return path to cat."""
    return CAT_PATH


@pytest.fixture
def cat_parser(cat_path: str = CAT_PATH) -> CatImgLinkHTMLParser:
    """Return parser stub."""
    return CatImgLinkHTMLParser(cat_path=cat_path)


@pytest.fixture
async def client() -> AsyncGenerator[TestClientProtocol, None]:
    """Server for testing."""
    app = server.create_app(server.get_config(parse=False))
    async with app.test_client() as c:
        yield c
