import re
from .constants import UNWANTED_WORDS

__all__ = ["sanitize_text", "clean_text", "to_float"]


def sanitize_text(text: str) -> str:
    """Sanitize text to remove unwanted characters

    Args:
        text (str): text to be sanitized

    Returns:
        str: sanitized text
    """

    try:
        words_to_remove = re.compile("|".join(UNWANTED_WORDS))
        text = words_to_remove.sub("", text)
        return text.strip()
    except Exception:
        return ""


def clean_text(text: str) -> str:
    """Clean text to remove unwanted characters

    Args:
        text (str): text to be cleared

    Returns:
        str: cleared text
    """
    try:
        text = re.sub(r"[\s.\-/]", "", sanitize_text(text))
        return text.strip()
    except Exception:
        return ""


def to_float(
    number: str, radix: str = ",", decimal_separator: str = ".", default: float = 0.0
) -> float:
    """Convert a string to floating point number

    First, remove the decimal separator.
    Then replace the radix separator with a dot.
    Finally convert the string to a float.

    Args:
        number (str): string to be converted
        radix (str, optional): radix point separator. Defaults to ",".
        decimal_separator (str, optional): decimal separator. Defaults to ".".
        defautl (float, optional): default value to return in case of error. Defaults to 0.0.

    Returns:
        float: converted string
    """
    number = sanitize_text(str(number))
    if number == "":
        return default

    try:
        return float(number.replace(decimal_separator, "").replace(radix, "."))
    except Exception:
        return default


def remove_consecutive_spaces(text: str | list[str]) -> str:
    """Remove consecutive spaces from a string

    Args:
        text (str): text to be cleaned

    Returns:
        str: cleaned text
    """
    text = " ".join(text) if isinstance(text, list) else text

    return re.sub(r"[\s\t\n ]+", " ", text).strip()


def is_valid_url(value: str) -> bool:
    """Check if a value is a URL.

    Args:
        value (str): The value to check.

    Returns:
        bool: True if the value is a URL, False otherwise.
    """
    return _has_access_key(value)


def _has_access_key(value: str) -> bool:
    """Check if a value has a NFC key.

    Args:
        value (str): The value to check.

    Returns:
        bool: True if the value has a NFC key, False otherwise.
    """
    return re.match(r".*\d{44}.*", value) is not None


def is_valid_access_key(value: str) -> bool:
    """Check if a value is a NFC key.

    Args:
        value (str): The value to check.

    Returns:
        bool: True if the value is a NFC key, False otherwise.
    """
    return len(value) == 44 and _has_access_key(value)
