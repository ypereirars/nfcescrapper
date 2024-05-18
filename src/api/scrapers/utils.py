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
        words_to_remove = "|".join(UNWANTED_WORDS)
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
        text = re.sub(r"[\s.\-/]", "", text)
        return text.strip()
    except Exception:
        return ""


def to_float(number: str, radix: str = ",", default: float = 0.0) -> float:
    """Convert a string to float point number

    Args:
        number (str): string to be converted
        radix (str, optional): radix point separator. Defaults to ",".
        defautl (float, optional): default value to return in case of error. Defaults to 0.0.

    Returns:
        float: converted string
    """
    number = sanitize_text(number)
    if number == "":
        return default

    try:

        return float(number.replace(radix, "."))
    except Exception:
        return default
