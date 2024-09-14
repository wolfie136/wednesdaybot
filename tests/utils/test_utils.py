import os
import uuid

import pytest
from freezegun import freeze_time

from utils.utils import is_it_wednesday, load_quotes_from_csv


@pytest.fixture
def setup_quote_file():
    temp_path = "/tmp/" + str(uuid.uuid4())
    with open(temp_path, "a") as temp_file:
        temp_file.write("quote number one;author\n")
        temp_file.write("quote number two;author two\n")
    yield temp_path
    os.remove(temp_path)


def test_load_quotes_from_csv(setup_quote_file):
    """
    Check that quotes get loaded
    """

    quotes = load_quotes_from_csv(setup_quote_file)
    expected_list = [
        {"quote": "quote number one", "attribution": "author"},
        {"quote": "quote number two", "attribution": "author two"},
    ]
    assert quotes == expected_list


@freeze_time("2024-08-21")
def test_is_it_wednesday_positive():
    assert is_it_wednesday() is True


@freeze_time("2024-08-23")
def test_is_it_wednesday_negative():
    assert is_it_wednesday() is False


@freeze_time("2024-08-23")
def test_is_it_wednesday_fake():
    assert is_it_wednesday(fake_wednesday=True) is True


@freeze_time("2024-08-23")
def test_is_it_wednesday_fake_env():
    os.environ["FAKE_WEDNESDAY"] = "something"
    assert is_it_wednesday() is True
