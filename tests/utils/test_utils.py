import os
import uuid

from utils.utils import load_quotes


def test_load_quoes():
    """
    Check that quotes get loaded
    """
    temp_path = "/tmp/" + str(uuid.uuid4())
    with open(temp_path, "a") as temp_file:
        temp_file.write("quote number one;author\n")
        temp_file.write("quote number two;author two\n")
    quotes = load_quotes(temp_path)
    expected_list = [
        {"quote": "quote number one", "attribution": "author"},
        {"quote": "quote number two", "attribution": "author two"},
    ]
    assert quotes == expected_list
    os.remove(temp_path)
