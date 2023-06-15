"""Test if we have a service worker."""


def test_worker(client):
    """Ensure we have a worker."""
    resp = client.get("/sw.js")
    assert resp.status == "200 OK"
