"""Test that cat is healthy."""

from hashlib import sha256

CAT_SHA256 = "85f77812c365c4cb02c1972fcbfa4c5b00a108bf12d6d34da5a84a8218a5219b"


def test_cat_linked_from_frontpage(client, cat_parser):
    """Ensure there is cat linked from the front page."""
    resp = client.get("/")
    assert resp.status == "200 OK"
    cat_parser.feed(str(resp.data))
    assert cat_parser.cat_count > 0


def test_cat_quality(client, cat_path):
    """Ensure that cat is purrfect."""
    resp = client.get(cat_path)
    assert resp.status == "200 OK"
    assert sha256(resp.data).hexdigest() == CAT_SHA256


def test_err(client):
    """Check if errors to happen."""
    resp = client.get("/404")
    assert resp.status == "404 NOT FOUND"
