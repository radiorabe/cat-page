"""Test for proper XcQ."""

import pytest


@pytest.mark.parametrize("endpoint", [("/.env"), ("/wp-login.php"), ("/wp-admin")])
async def test_rick(client, endpoint):
    """Ensure we redirect hackers properly."""
    resp = await client.get(endpoint, follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers.get("location") == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
