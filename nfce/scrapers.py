from bs4 import BeautifulSoup
from .parsers import Parser, NfeParser
from .models import NotaFiscalEletronica
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .browsers import get_browser

__all__ = ["NfeScraper"]


class NfeScraper:
    """NFe - Nota Fiscal Eletrônica.
    Create a webscraper and transform data present in an invoice QR
    Code into a python dictionary.
    """

    def __init__(
        self,
        content_parser: Parser,
        browser: WebDriver,
        id_to_wait="tabResult",
        wait_timeout=5,
    ):
        """Configures an invoice processor.

        Args:
            chromedriver_path (str, optional): chrome webdriver path location.
            Defaults to "chromedriver" assuming it's present in path variable.
            id_to_wait (str, optional): HTML id that the scraper must wait on
            to start loading page. Defaults to "tabResult".
            wait_timeout (int, optional): how long to wait until it times out.
            Defaults to 5.
        """
        self.content_parser = content_parser
        self.timeout = wait_timeout
        self.id_to_wait = id_to_wait
        self.browser = browser

    def scrap(self, url: str) -> NotaFiscalEletronica:
        try:
            self.browser.get(url)
            page = self._get_page_data()
            nfe_data = self.content_parser.parse(page)
        except TimeoutException:
            print("Timed out waiting for page to load")
            nfe_data = None

        return nfe_data

    def _get_page_data(self) -> BeautifulSoup:
        """Get data from an invoice page

        Args:
            browser (WebDriver): web browser

        Returns:
            BeautifulSoup: html page
        """
        element_present = EC.presence_of_element_located((By.ID, self.id_to_wait))
        WebDriverWait(self.browser, self.timeout).until(element_present)
        source = self.browser.page_source
        data = BeautifulSoup(source, "html.parser")

        return data


def read_invoice(url: str) -> dict:
    """Reads an invoice from a given URL.

    Args:
        url (str): URL to scrap.

    Returns:
        dict: invoice data.
    """
    with get_browser() as browser:
        scraper = NfeScraper(NfeParser(), browser)
        data = scraper.scrap(url)

        return vars(data) if data else {}
