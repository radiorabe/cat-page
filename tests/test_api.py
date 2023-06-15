"""Test that we have an api endpoint."""


def test_api(client):
    """Ensure we have an api."""
    resp = client.get("/api")
    assert resp.status == "200 OK"
