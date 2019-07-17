def test_worker(client):
    """Ensure we have an api."""
    resp = client.get("/api")
    assert resp.status == "200 OK"
