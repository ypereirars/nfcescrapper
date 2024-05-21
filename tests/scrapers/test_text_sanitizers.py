from src.scrapers.utils import (
    remove_consecutive_spaces,
    to_float,
    sanitize_text,
    clean_text,
)
import pytest


@pytest.mark.parametrize(
    "input_text,expected_output",
    [
        ("Hello     world", "Hello world"),
        ("Hello world", "Hello world"),
        ("   Hello world   ", "Hello world"),
        ("This    is    a    test", "This is a test"),
        ("     ", ""),
    ],
)
def test_remove_consecutive_spaces(input_text, expected_output):
    assert remove_consecutive_spaces(input_text) == expected_output


@pytest.mark.parametrize(
    "input_text,expected_output",
    [
        ("10,0", 10.0),
        ("10", 10.0),
        ("10,5", 10.5),
        ("10,5 ", 10.5),
        (" 10,5 ", 10.5),
    ],
)
def test_to_float_with_comma_radix(input_text, expected_output):
    assert to_float(input_text, radix=",") == expected_output


@pytest.mark.parametrize(
    "input_text,expected_output",
    [
        ("10.0", 10.0),
        ("10", 10.0),
        ("10.5", 10.5),
        ("10.5 ", 10.5),
        (" 10.5 ", 10.5),
    ],
)
def test_to_float_with_dot_radix(input_text, expected_output):
    assert to_float(input_text, radix=".") == expected_output


def test_to_float_default_value_when_invalid_string():
    assert to_float("invalid") == 0.0


@pytest.mark.parametrize(
    "input_text,expected_output",
    [
        ("\r\t\n", ""),
        ("\r\t\ntest", "test"),
        ("(TEST)", "TEST"),
    ],
)
def test_sanitize_text_special_chars(input_text, expected_output):
    assert sanitize_text(input_text) == expected_output


@pytest.mark.parametrize(
    "input_text,expected_output",
    [
        ("UN:    123", "123"),
        ("Vl. Unit.: 123,45", "123,45"),
        ("Qtde.: 1230", "1230"),
        ("Código: 123040", "123040"),
        ("CNPJ: 12.345.678/00001-23", "12.345.678/00001-23"),
    ],
)
def test_sanitize_text_unwanted_words(input_text, expected_output):
    assert sanitize_text(input_text) == expected_output


@pytest.mark.parametrize(
    "input_text,expected_output",
    [
        ("\t\t\rUN:    123", "123"),
        ("(Vl. Unit.: 123,45", "123,45"),
        ("Qtde.:\n\n\t1230", "1230"),
        ("\t\t\tCódigo: \n\n\n123040", "123040"),
        ("\r\r\rCNPJ: \t\t\t12.345.678/00001-23", "12.345.678/00001-23"),
        ("A SIMPLE TEST WITH SPACE", "A SIMPLE TEST WITH SPACE"),
    ],
)
def test_sanitize_text_unwanted_words_with_special_chars(input_text, expected_output):
    assert sanitize_text(input_text) == expected_output


@pytest.mark.parametrize(
    "input_text,expected_output",
    [
        ("\t\t\rUN:    123", "123"),
        ("(Vl. Unit.: 1.123,45", "1123,45"),
        ("Qtde.:\n\n\t1.230", "1230"),
        ("\t\t\tCódigo: \n\n\n123040", "123040"),
        ("\r\r\rCNPJ: \t\t\t12.345.678/00001-23", "123456780000123"),
        ("A SIMPLE TEST WITH SPACE", "ASIMPLETESTWITHSPACE"),
    ],
)
def test_clean_text_removing_dots_dashes_whitespace(input_text, expected_output):
    assert clean_text(input_text) == expected_output
