import re
from datetime import datetime
from nfce.models import (Company,
                         EletronicInvoice,
                         PaymentTotals,
                         Product)


UNWANTED_WORDS = [r"UN: *", r"Vl. Unit.:", r"Qtde.:", r"Código:", r"CNPJ:", r"\(", r"\)", r"\n", r"\r", r"\t"]
UNWANTED_WORDS_REGEX = re.compile('|'.join(UNWANTED_WORDS))


def get_totals_info(totals: list, payment_type: str) -> dict:

    values = {}
    for total in totals:
        if total.find('label') is None:
            continue

        key = sanitize_text(total.find('label').string)

        if key == payment_type:
            continue

        key = 'tax' if 'Tributos Totais' in key else key.replace('R$:', '').strip()

        value = to_float(total.find('span').text)
        values[key] = value

    return values

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

    def __init__(self, content_selector='conteudo', info_selector='infos'):
        self.content_selector = content_selector
        self.info_selector = info_selector
        self.page = None
        self.content = None

    def parse(self, page) -> EletronicInvoice:
        self.page = page
        self.content = self.page.find("div", id=self.content_selector)
        self.info = self.page.find("div", id=self.info_selector)

        company = self._get_company()
        totals = self._get_totals()
        items = self._get_items()
        general_info = self._get_general_info()

        invoice = EletronicInvoice(company, items, totals, **general_info)

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

        totals = self.content.find_all("div", id="linhaTotal")
        payment_type = sanitize_text(self.content.find_all("label", class_="tx")[0].text)

        values = get_totals_info(totals, payment_type)

        total_items = int(values.get('Qtd. total de itens:', 0))
        total_after_discount = values.get('Valor a pagar', 0)
        discounts = values.get('Descontos', 0)
        total_before_discount = values.get('Valor total', total_after_discount-discounts)
        payment_type = sanitize_text(payment_type)
        exchange = values.get('Troco', 0)
        tax = values.get('tax', 0)

        return PaymentTotals(exchange, tax, payment_type, total_before_discount, total_after_discount, total_items, discounts)

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

        items = {}
        not_processed_items = 0
        for i in range(0, qty):
            try:
                code = sanitize_text(codes[i].text)
                if code in items.keys():
                    items[code].quantity += to_float(quantities[i].text)
                    items[code].total_price = items[code].quantity * items[code].price
                else:
                    product = Product(code,
                            sanitize_text(products[i].text),
                            to_float(unitary_prices[i].text),
                            to_float(quantities[i].text),
                            unity_of_measure=sanitize_text(uoms[i].text),
                            total_price=to_float(total_prices[i].text))
                    items[code] = product
            except Exception as ex:
                not_processed_items += 1

        if not_processed_items > 0:
            raise Exception(f"{not_processed_items} items could not be processed")

        return list(items.values())

    def _get_general_info(self) -> dict:
        """Get general information from an invoice

        Returns:
            dict: general information
        """

        try:
            access_key = sanitize_text(self.info.find("span", class_="chave").text)
            access_key = ''.join(access_key.split(' '))
            contents = self.info.find('ul', class_='ui-listview').find('li').contents
            contents = list(filter(lambda el: el != '\n' and el.name != 'br' and el.name != 'strong', contents))

            date = contents[2].split('\n')[0]
            date = ''.join(date.rsplit(':', 1)) # remove last occurrency of : and join to form the timezone
            general_info = {
                'access_key': access_key,
                'number': contents[0],
                'serie': contents[1],
                'issue_date': datetime.strptime(date, '%d/%m/%Y %H:%M:%S%z')
            }
        except:
            general_info = {
                'access_key': '',
                'number': '',
                'serie': '',
                'issue_date': ''
            }

        return general_info
