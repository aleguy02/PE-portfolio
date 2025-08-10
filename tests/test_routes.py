"""
Tests for non-API routes
"""

import pytest


def test_bad_route(client):
    response = client.get("/bad")
    assert "<h1>Oops! There's nothing to see here</h1>" in response.get_data(
        as_text=True
    )


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    headers = dict(response.headers)

    assert "<title>Alejandro Villate</title>" in html
    assert "<h1>Alejandro Villate</h1>" in html
    assert '<div class="profile">' in html
    assert "Computer Science major at the University of Florida" in html
    assert '<div class="profile">' in html
    assert '<div id="map"></div>' in html
    assert headers["Content-Type"] == "text/html; charset=utf-8"


def test_hobbies(client):
    response = client.get("/hobbies")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    headers = dict(response.headers)

    assert '<section class="hobbies-section section">' in html
    assert headers["Content-Type"] == "text/html; charset=utf-8"
