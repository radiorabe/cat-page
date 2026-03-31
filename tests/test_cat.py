"""Test that cat is healthy."""

from hashlib import sha256

CAT_SHA256 = "85f77812c365c4cb02c1972fcbfa4c5b00a108bf12d6d34da5a84a8218a5219b"


async def test_cat_linked_from_frontpage(client, cat_parser):
    """Ensure there is cat linked from the front page."""
    resp = await client.get("/")
    assert resp.status_code == 200
    cat_parser.feed(await resp.get_data(as_text=True))
    assert cat_parser.cat_count > 0


async def test_cat_quality(client, cat_path):
    """Ensure that cat is purrfect."""
    resp = await client.get(cat_path)
    assert resp.status_code == 200
    assert sha256(await resp.get_data()).hexdigest() == CAT_SHA256


async def test_err(client):
    """Check if errors to happen."""
    resp = await client.get("/404")
    assert resp.status_code == 404
