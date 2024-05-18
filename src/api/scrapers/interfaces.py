from abc import ABC, abstractmethod
from typing import Any


class Parser(ABC):
    CONTENT_SELECTOR = ""

    @abstractmethod
    def parse(self, page) -> dict[str, Any]:
        pass


class Scraper(ABC):
    @abstractmethod
    def get(self, url: str) -> dict[str, Any]:
        """Get data from an URL and return it as a dictionary if a parser is provided, otherwise return the raw data.

        Args:
            url (str): URL to scrape

        Returns:
            dict[str, Any]: Scraped data
        """
        raise NotImplementedError("Method 'get' must be implemented")

    @abstractmethod
    def wait_page_load(self) -> None:
        """Wait for the page to load"""
        pass
