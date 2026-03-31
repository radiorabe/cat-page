"""Test if we have a service worker."""


async def test_worker(client):
    """Ensure we have a worker."""
    resp = await client.get("/sw.js")
    assert resp.status_code == 200
