from src.scrapers.utils import is_valid_url, is_valid_access_key
import pytest


def test_is_valid_url_return_false_when_does_not_contain_access_key():
    invalid_input = "www.google.com"

    assert not is_valid_url(invalid_input)


def test_is_valid_url_return_true_when_url_contains_access_key():
    valid_input = "https://www.google.com/12345678901234567890123456789012345678901234"

    assert is_valid_url(valid_input)


def test_is_valid_access_key_return_true_when_value_has_44_digits():
    valid_input = "12345678901234567890123456789012345678901234"

    assert is_valid_access_key(valid_input)


@pytest.mark.parametrize(
    "invalid_input",
    [
        "A2345678901234567890123456789012345678901234",  # length 44 but not only digits
        "ASDFGHJKLOIUytrewASXCv mkuy654wsasxcgh@#$^%&*(*)",
        "A2345678901234567890123456789012345678901234A2345678901234567890123456789012345678901234",
    ],
)
def test_is_valid_access_key_return_false_when_value_has_not_44_digits(invalid_input):
    assert not is_valid_access_key(invalid_input)
