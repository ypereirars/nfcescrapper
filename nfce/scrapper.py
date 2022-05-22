
from bs4 import BeautifulSoup
from nfce.browsers import get_chrome_browser
from nfce.parser import NFCeParser
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class NfeScrapper():
    """NFe - Nota Fiscal Eletrônica.
    Create a webscrapper and transform data present in an invoice QR
    Code into a python dictionary.
    """

    def __init__(self,
                 content_parser: NFCeParser,
                 id_to_wait="tabResult",
                 wait_timeout=5):
        """Configures an invoice processor.

        Args:
            chromedriver_path (str, optional): chrome webdriver path location.
            Defaults to "chromedriver" assuming it's present in path variable.
            id_to_wait (str, optional): HTML id that the scrapper must wait on
            to start loading page. Defaults to "tabResult".
            wait_timeout (int, optional): how long to wait until it times out.
            Defaults to 5.
        """
        self.content_parser = content_parser
        self.timeout = wait_timeout
        self.id_to_wait = id_to_wait

    def get(self, url: str):
        with get_chrome_browser() as browser:
            try:
                browser.get(url)
                page = self._get_page_data(browser)
                nfe_data = self.content_parser.parse(page)
            except TimeoutException:
                print("Timed out waiting for page to load")
                nfe_data = None

        return nfe_data

    def _get_page_data(self, browser: WebDriver) -> BeautifulSoup:
        """ Get data from an invoice page

        Args:
            browser (WebDriver): web browser

        Returns:
            BeautifulSoup: html page
        """
        element_present = EC.presence_of_element_located((By.ID, self.id_to_wait))
        WebDriverWait(browser, self.timeout).until(element_present)
        source = browser.page_source
        data = BeautifulSoup(source, 'html.parser')

        return data
