"""Test that we have an api endpoint."""

from app import server


async def test_api(client):
    """Ensure we have an api."""
    resp = await client.get("/api")
    assert resp.status_code == 200


async def test_create_app_defaults():
    """Ensure create_app works without an explicit config (factory mode)."""
    app = server.create_app()
    assert app is not None
