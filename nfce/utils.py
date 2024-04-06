import re
import json

UNWANTED_WORDS = [
    r"UN: *",
    r"Vl. Unit.:",
    r"Qtde.:",
    r"Código:",
    r"CNPJ:",
    r"\(",
    r"\)",
    r"\n",
    r"\r",
    r"\t",
]
UNWANTED_WORDS_REGEX = re.compile("|".join(UNWANTED_WORDS))


def sanitize_text(text: str) -> str:
    """Sanitize text to remove unwanted characters

    Args:
        text (str): text to be sanitized

    Returns:
        str: sanitized text
    """

    try:
        text = UNWANTED_WORDS_REGEX.sub("", text)
        return text.strip()
    except:
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
    except:
        return default


def save_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as outfile:
        return json.dump(data, outfile, ensure_ascii=False, indent=4)
