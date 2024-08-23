import json

import pytest

from src.api import app


@pytest.fixture()
def client():
    return app.test_client()


def test_request_quote(client):
    response = client.get("/v1/quote")
    response_object = json.loads(response.data)
    assert len(response_object) > 0
    for quote in response_object:
        assert len(quote.keys()) == 2
        assert "quote" in quote
        assert "attribution" in quote


def test_request_quote_random(client):
    response = client.get("/v1/quote/random")
    quote = json.loads(response.data)
    assert len(quote.keys()) == 2
    assert "quote" in quote
    assert "attribution" in quote


def test_request_quote_index(client):
    with open("wednesday.csv") as csvfile:
        quote_count = sum(1 for _ in csvfile)

    # Check we can get all the available quotes in the file
    index_counter = 0
    while index_counter < quote_count:
        response = client.get(f"/v1/quote/{index_counter}")
        quote = json.loads(response.data)
        assert len(quote.keys()) == 2
        assert "quote" in quote
        assert "attribution" in quote
        index_counter += 1

    # When getting a higher index we get an error
    response = client.get(f"/v1/quote/{index_counter}")
    quote = json.loads(response.data)
    assert len(quote.keys()) == 1
    assert quote["error"] == "Quote not found!"
