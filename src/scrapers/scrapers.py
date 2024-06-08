from typing import Any
from bs4 import BeautifulSoup

from scrapers.browsers import get_browser
from scrapers.parsers import NfceParser
from .interfaces import Parser, Scraper
from selenium.common.exceptions import TimeoutException as WebDriverTimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

__all__ = ["NfceScraper"]


class NfceScraper(Scraper):
    """NFCe - Nota Fiscal do Consumidor Eletrônica.
    Create a webscraper and transform data present in an invoice QR Code into a python dictionary.
    """

    def __init__(
        self,
        browser: WebDriver = None,
        parser: Parser = NfceParser(),
        id_to_wait: str = "tabResult",
        timeout: int = 5,
    ):
        """
        Initializes a Scraper object.

        Args:
            browser (WebDriver): The web driver object used to interact with the browser. Defaults to None.
            parser (Parser, optional): The content parser object used to parse the scraped data. Defaults to NfceParser.
            id_to_wait (str, optional): The ID of the element to wait for before scraping. Defaults to "tabResult".
            timeout (int, optional): The maximum time, in seconds, to wait for the element to appear. Defaults to 5.
        """
        self.parser = parser
        self.timeout = timeout
        self.id_to_wait = id_to_wait
        self.browser = browser or get_browser()

    def get(self, url: str) -> dict[str, Any]:
        try:
            self.browser.get(url)
            self.wait_page_load()
            page = self._get_page()
            data = self.parser.parse(page)
            return data

        except WebDriverTimeoutException as e:
            raise TimeoutError(f"Timed out after waitging browser to load for {self.timeout}s.") from e

        finally:
            self.browser.quit()

    def _get_page(self) -> BeautifulSoup:
        source = self.browser.page_source
        soup = BeautifulSoup(source, "html.parser")

        return soup

    def wait_page_load(self) -> None:
        if not self.id_to_wait:
            return

        at_given_id = (By.ID, self.id_to_wait)
        element_is_present = EC.presence_of_element_located(at_given_id)
        WebDriverWait(self.browser, self.timeout).until(element_is_present)
