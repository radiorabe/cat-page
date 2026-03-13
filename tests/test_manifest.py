"""Test that the web app manifest meets PWA icon requirements."""

import json


def test_manifest_has_192_icon(client):
    """Ensure manifest contains a 192x192 PNG icon for homescreen use."""
    resp = client.get("/static/manifest.json")
    assert resp.status == "200 OK"
    data = json.loads(resp.data)
    sizes = [icon["sizes"] for icon in data.get("icons", [])]
    assert "192x192" in sizes


def test_manifest_has_512_icon(client):
    """Ensure manifest contains a 512x512 PNG icon for splash screen use."""
    resp = client.get("/static/manifest.json")
    assert resp.status == "200 OK"
    data = json.loads(resp.data)
    sizes = [icon["sizes"] for icon in data.get("icons", [])]
    assert "512x512" in sizes


def test_icon_192_accessible(client):
    """Ensure the 192x192 PNG icon is served correctly."""
    resp = client.get("/static/icon-192.png")
    assert resp.status == "200 OK"
    assert resp.content_type == "image/png"


def test_icon_512_accessible(client):
    """Ensure the 512x512 PNG icon is served correctly."""
    resp = client.get("/static/icon-512.png")
    assert resp.status == "200 OK"
    assert resp.content_type == "image/png"


def test_favicon_svg_accessible(client):
    """Ensure the SVG favicon is served correctly."""
    resp = client.get("/static/icon.svg")
    assert resp.status == "200 OK"


def test_apple_touch_icon_accessible(client):
    """Ensure the Apple touch icon is served correctly."""
    resp = client.get("/static/apple-touch-icon.png")
    assert resp.status == "200 OK"
    assert resp.content_type == "image/png"


def test_frontpage_has_favicon_links(client):
    """Ensure the front page references the favicon and apple-touch-icon."""
    resp = client.get("/")
    assert resp.status == "200 OK"
    html = resp.data.decode()
    assert "/static/icon.svg" in html
    assert "/static/apple-touch-icon.png" in html


def test_background_svg_accessible(client):
    """Ensure the local SVG background is served correctly."""
    resp = client.get("/static/background.svg")
    assert resp.status == "200 OK"
