class StrCleaner():
    """String sanitizer
    """
    def __init__(self):
        pass

    def to_float(self, string, radix=","):
        """Convert a string to float point number

        Args:
            string (str): string to be converted
            radix (str, optional): radix point separator. Defaults to ",".

        Returns:
            [type]: [description]
        """
        return float(string.replace(radix, "."))

    def remove_whitechars(self, string):
        """Removes all white characters from a string, such as \\t and \\n

        Args:
            string ([str]): string to be sanitized

        Returns:
            [str]: sanitized string
        """
        return " ".join(string.split())
