import json

import pytest

from src.api import app


@pytest.fixture()
def client():
    return app.test_client()


def test_request_quote(client):
    response = client.get("/v1/quotes")
    response_object = json.loads(response.data)
    assert len(response_object) > 0
    for quote in response_object["data"]:
        assert len(quote.keys()) == 4
        assert "text" in quote
        assert "attribution" in quote
        assert "id" in quote
        assert "added" in quote
    assert "next" in response_object["links"].keys()
    assert "self" in response_object["links"].keys()


def test_request_quote_random(client):
    response = client.get("/v1/quotes/random")
    quote = json.loads(response.data)["data"]
    assert len(quote.keys()) == 4
    assert "text" in quote
    assert "attribution" in quote
    assert "id" in quote
    assert "added" in quote


def test_request_quote_id(client):
    index_response = client.get("/v1/quotes")
    index_response_object = json.loads(index_response.data)
    for index_quote in index_response_object["data"]:
        response = client.get(f"/v1/quotes/{index_quote["id"]}")
        quote = json.loads(response.data)["data"]
        assert len(quote.keys()) == 4
        assert "text" in quote
        assert "attribution" in quote
        assert "id" in quote
        assert "added" in quote

    # When getting an invalid id we get an error
    response = client.get("/v1/quotes/randomshiz")
    response_json = json.loads(response.data)
    print(response_json)
    assert len(response_json.keys()) == 1
    assert response_json["error"] == "Quote not found!"
