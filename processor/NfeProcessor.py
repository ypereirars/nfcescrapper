from utils.strcleaner import StrCleaner
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class NfeProcessor():
    """NFe - Nota Fiscal Eletrônica.
    Create a webscrapper and transform data present in an invoice QR
    Code into a python dictionary.
    """
    def __init__(self, 
        chromedriver_path="chromedriver", 
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
        self.chromedriver_path = chromedriver_path
        self.timeout = wait_timeout
        self.id_to_wait = id_to_wait
        self.strprocessor = StrCleaner()

    def process(self, url):
        """Process information from an invoice URL provided.

        Args:
            url (URL): url to be scrapped

        Returns:
            [dict]: a dictionary of an invoice
        """
        self.__set_browser()
        self.browser.get(url)

        try:
            page_data = self.__get_data()
            content = page_data.find("div", id="conteudo")
            nfe_data = self.__process_table(content)
            
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            self.browser.close()
        
        return nfe_data
    
    def __set_browser(self):
        """Configure information for chrome webdriver, setting it to work in silence.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.browser = webdriver.Chrome(executable_path=self.chromedriver_path, chrome_options=options)

    def __get_data(self):
        """Scrap data from an website and get invoice information

        Returns:
            [dict]: invoice dictionary
        """
        element_present = EC.presence_of_element_located((By.ID, self.id_to_wait))
        WebDriverWait(self.browser, self.timeout).until(element_present)

        source = self.browser.page_source
        data = bs(source, 'html.parser')
        return data

    def __process_table(self, content):
        """Process a table of contents

        Args:
            content (BeautifullSoup): an html div where table content is located

        Returns:
            [dict]: a dictionary contaning all information about an invoice
        """
        info = content.find_all("div", class_="text")
        totals = self.__get_totals(content)
        data = {
            "company_name": self.__sanitize_text(content.find_all("div", class_="txtTopo")[0].text),
            "cnpj": self.__sanitize_text(info[0].text),
            "address": self.__sanitize_text(info[1].text),
            **totals,
            "items": self.__get_items(content),
        }

        return data

    def __get_totals(self, content):
        """Get all totals from an invoice

        Args:
            content (BeautifullSoup): an html div where table content is located

        Returns:
            [dict]: a dictionary contaning totals information
        """
        totals = content.find_all("span", class_="totalNumb")
        how_paid = content.find_all("label", class_="tx")[0].text

        return {
            "total_items": self.__sanitize_number(totals[0].text),
            "total_value": self.__sanitize_number(totals[1].text),
            "discounts": self.__sanitize_number(totals[2].text),
            "total_to_pay": self.__sanitize_number(totals[3].text),
            "how_paid": self.__sanitize_text(how_paid),
            "total_paied": self.__sanitize_number(totals[5].text),
            "exchange": self.__sanitize_number(totals[6].text),
            "taxes": self.__sanitize_number(totals[7].text)
        }

    def __get_items(self, content):
         """Get items from eletronic invoice

        Args:
            content (BeautifullSoup): an html div where table content is located

        Returns:
            [list]: list contaning all produts information
        """
        table = content.find("table", id="tabResult")
        products = table.find_all("span", class_="txtTit")
        codes = table.find_all("span", class_="RCod")
        quantities = table.find_all("span", class_="Rqtd")
        uoms = table.find_all("span", class_="RUN")
        unitary_prices = table.find_all("span", class_="RvlUnit")
        total_prices = table.find_all("span", class_="valor")

        qty = len(products)

        try:
            items = []
            for i in range(0, qty):
                items.append({
                    "product": self.__sanitize_text(products[i].text),
                    "code": self.__sanitize_text(codes[i].text),
                    "quantity":self.__sanitize_number(quantities[i].text),
                    "uom": self.__sanitize_text(uoms[i].text),
                    "unitary_price": self.__sanitize_number(unitary_prices[i].text),
                    "total": self.__sanitize_number(total_prices[i].text)
                })

            return items
        except:
            raise "Could not process items"
    
    def __sanitize_number(self, number):
        """Sanitize and transform a string to float

        Args:
            number (float): number to be sanitized

        Returns:
            float: sanitized number
        """
        try:
            return self.strprocessor.to_float(self.__sanitize_text(number))
        except:
            return 0.0

    def __sanitize_text(self, string):
        """ Sanitize a string removing all specific texts from strings

        Args:
            string (string): string to be sanitized

        Returns:
            string: sanitized string
        """
        try:
            string = string.replace("UN: ", "")\
                    .replace("Vl. Unit.:", "")\
                    .replace("UN: ", "")\
                    .replace("Qtde.:", "")\
                    .replace("Código:", "")\
                    .replace("CNPJ:", "")\
                    .replace("(", "").replace(")", "")
            return self.strprocessor.remove_whitechars(string)
        except:
            return ""