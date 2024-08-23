import os
import uuid

import pytest

from utils.utils import load_quotes


@pytest.fixture
def setup_quote_file():
    temp_path = "/tmp/" + str(uuid.uuid4())
    with open(temp_path, "a") as temp_file:
        temp_file.write("quote number one;author\n")
        temp_file.write("quote number two;author two\n")
    yield temp_path
    os.remove(temp_path)


def test_load_quoes(setup_quote_file):
    """
    Check that quotes get loaded
    """

    quotes = load_quotes(setup_quote_file)
    expected_list = [
        {"quote": "quote number one", "attribution": "author"},
        {"quote": "quote number two", "attribution": "author two"},
    ]
    assert quotes == expected_list
