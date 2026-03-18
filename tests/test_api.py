"""Test that we have an api endpoint."""

from app import server


def test_api(client):
    """Ensure we have an api."""
    resp = client.get("/api")
    assert resp.status_code == 200


def test_create_app_defaults():
    """Ensure create_app works without an explicit config (factory mode)."""
    app = server.create_app()
    assert app is not None
