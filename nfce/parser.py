import re
from nfce.models import (Company,
                         EletronicInvoice,
                         PaymentTotals,
                         Product)


UNWANTED_WORDS = [r"UN: *", r"Vl. Unit.:", r"Qtde.:", r"Código:", r"CNPJ:", r"\(", r"\)", r"\n", r"\r", r"\t"]
UNWANTED_WORDS_REGEX = re.compile('|'.join(UNWANTED_WORDS))


def sanitize_text(text: str) -> str:
    """Sanitize text to remove unwanted characters

    Args:
        text (str): text to be sanitized

    Returns:
        str: sanitized text
    """

    try:
        text = UNWANTED_WORDS_REGEX.sub('', text)
        return text.strip()
    except:
        return ""


def to_float(number: str, radix: str = ',') -> float:
    """ Convert a string to float point number

    Args:
        number (str): string to be converted
        radix (str, optional): radix point separator. Defaults to ",".

    Returns:
        float: converted string
    """
    number = sanitize_text(number)

    return float(number.replace(radix, "."))


class NFCeParser():

    def __init__(self, content_selector='conteudo'):
        self.content_selector = content_selector
        self.page = None
        self.content = None

    def parse(self, page) -> EletronicInvoice:
        self.page = page
        self.content = self.page.find("div", id=self.content_selector)

        company = self._get_company()
        totals = self._get_totals()
        items = self._get_items()

        invoice = EletronicInvoice(company, items, totals)

        return invoice

    def _get_company(self) -> Company:
        """ Get company data from an invoice content

        Returns:
            Company: company data
        """
        info = self.content.find_all("div", class_="text")
        company = Company(sanitize_text(self.content.find_all("div", class_="txtTopo")[0].text),
                          sanitize_text(info[0].text),
                          sanitize_text(info[1].text))
        return company

    def _get_totals(self) -> PaymentTotals:
        """Get all totals from an invoice

        Returns:
            PaymentTotals: totals information
        """
        totals = self.content.find_all("span", class_="totalNumb")
        payment_type = self.content.find_all("label", class_="tx")[0].text

        total_items = to_float(totals[0].text)
        total_price = to_float(totals[1].text)
        discounts = to_float(totals[2].text)
        total_to_pay = to_float(totals[3].text)
        payment_type = sanitize_text(payment_type)
        total_paid = to_float(totals[5].text)
        exchange = to_float(totals[6].text)
        tax = to_float(totals[7].text)

        return PaymentTotals(exchange, tax, payment_type, total_paid, total_to_pay, total_price, total_items, discounts)

    def _get_items(self) -> list:
        """Get items from eletronic invoice

        Args:
            content (BeautifullSoup): an html div where table content is located

        Returns:
            [list]: list contaning all produts information
        """
        table = self.content.find("table", id="tabResult")
        products = table.find_all("span", class_="txtTit")
        codes = table.find_all("span", class_="RCod")
        quantities = table.find_all("span", class_="Rqtd")
        uoms = table.find_all("span", class_="RUN")
        unitary_prices = table.find_all("span", class_="RvlUnit")
        total_prices = table.find_all("span", class_="valor")

        qty = len(products)

        items = []
        not_processed_items = 0
        for i in range(0, qty):
            try:
                product = Product(sanitize_text(codes[i].text),
                            sanitize_text(products[i].text),
                            to_float(unitary_prices[i].text),
                            to_float(quantities[i].text),
                            unity_of_measure=sanitize_text(uoms[i].text),
                            total_price=to_float(total_prices[i].text))
                items.append(product)
            except Exception as ex:
                not_processed_items += 1

        if not_processed_items > 0:
            raise Exception(f"{not_processed_items} items could not be processed")

        return items
