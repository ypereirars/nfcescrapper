from abc import ABC, abstractmethod
from typing import Any

__all__ = ["Parser", "ContentParser", "InfoParser", "Scraper"]


class Parser(ABC):
    CONTENT_SELECTOR = ""

    @abstractmethod
    def parse(self, page) -> dict[str, Any]:
        pass

    def _get_content(self, page: Any) -> Any:
        if not self.CONTENT_SELECTOR:
            raise ValueError("CONTENT_SELECTOR must be defined")

        return page.find("div", id=self.CONTENT_SELECTOR)


class ContentParser(Parser):
    CONTENT_SELECTOR = "conteudo"


class InfoParser(Parser):
    CONTENT_SELECTOR = "infos"


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
