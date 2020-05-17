import pytest


@pytest.mark.parametrize("endpoint", [("/.env"), ("/wp-login.php"), ("/wp-admin")])
def test_rick(client, endpoint):
    """Ensure we redirect hackers properly."""
    resp = client.get(endpoint)
    assert resp.status == "302 FOUND"
    assert resp.headers.get("Location") == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
