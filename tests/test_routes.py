import pytest


def test_bad_route(client):
    response = client.get("/bad")
    assert "<h1>Oops! There's nothing to see here</h1>" in response.get_data(
        as_text=True
    )
