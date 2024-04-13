import re
from typing import Dict
from datetime import datetime
from nfce.models import (
    Empresa,
    Endereco,
    Item,
    Totais,
    NotaFiscalEletronica,
    InformacoesNota,
    Produto,
    Tributacao,
    TipoPagamento,
)
from .utils import to_float, sanitize_text, clean_text


from abc import ABC, abstractmethod


class Parser(ABC):
    CONTENT_SELECTOR = ""

    @abstractmethod
    def parse(self, page):
        pass


class EmpresaParser(Parser):
    CONTENT_SELECTOR = "conteudo"

    def parse(self, page) -> Empresa:
        self.content = page.find("div", id=self.CONTENT_SELECTOR)
        company = self._get_company()
        return company

    def _get_company(self) -> Empresa:
        """Get company data from an invoice content

        Returns:
            Company: company data
        """
        info = self.content.find_all("div", class_="text")
        address = self._get_address(info)
        name = self.content.find_all("div", class_="txtTopo")[0].text

        company = Empresa(
            sanitize_text(name).upper(),
            clean_text(sanitize_text(info[0].text)),
            address,
        )
        return company

    def _get_address(self, info):
        address_text = sanitize_text(sanitize_text(info[1].text))
        try:
            address = address_text.upper().split(",")
            assert len(address[4]) == 2

            address = Endereco(
                address[0],
                address[1],
                address[2],
                address[3],
                address[4],
                address[5],
            )
        except:
            address = Endereco(address_text)
        return address


class InformacoesNotaParser(Parser):
    CONTENT_SELECTOR = "infos"

    def parse(self, page) -> dict:
        self.content = page.find("div", id=self.CONTENT_SELECTOR)
        info = self._get_info()
        return info

    def _get_info(self) -> dict:
        """Get general information from an invoice

        Returns:
            dict: general information
        """

        try:
            access_key = sanitize_text(self.content.find("span", class_="chave").text)
            contents = self.content.find("ul", class_="ui-listview").find("li").contents
            contents = list(
                filter(
                    lambda el: el != "\n" and el.name != "br" and el.name != "strong",
                    contents,
                )
            )

            date = contents[2].split("\n")[0]
            date = "".join(date.rsplit(":", 1))
            authorization_protocol = (
                contents[3].replace("às", "").replace("\n", "").split(" ")
            )
            protocol, authorization_date = (
                authorization_protocol[0],
                authorization_protocol[1:],
            )
            authorization_date = " ".join(
                string for string in authorization_date if len(string) > 0
            )
            authorization_date = datetime.strptime(
                authorization_date, "%d/%m/%Y %H:%M:%S%z"
            )

            tax = self._get_tax_info()

            info = InformacoesNota(
                clean_text(access_key),
                contents[0],
                contents[1],
                datetime.strptime(date, "%d/%m/%Y %H:%M:%S%z"),
                protocol,
                authorization_date,
                tax,
            )

        except Exception as ex:
            info = InformacoesNota(
                "",
                "",
                "",
                None,
            )

        return info

    def _get_tax_info(self):
        taxpayer_info = self.content.findAll("div")[-3].find("ul").text.strip()
        regex = re.compile(
            r"trib *aprox: *R\$ *(\d+[.,]\d+) *fed *R\$ *(\d+[.,]\d+) *est *R\$ *(\d+[.,]\d+) *mun *fonte: *(\w+)",
            re.IGNORECASE,
        )
        matches = regex.match(taxpayer_info)

        if not matches:
            attribute = self.content.parent.find("span", class_="totalNumb txtObs")
            tax = to_float(attribute.text) if attribute else 0.0
            return Tributacao(federal=tax)

        return Tributacao(
            to_float(matches.group(1)),
            to_float(matches.group(2)),
            to_float(matches.group(3)),
            matches.group(4),
        )


class ItensParser(Parser):
    CONTENT_SELECTOR = "conteudo"

    def parse(self, page) -> list:
        self.content = page.find("div", id=self.CONTENT_SELECTOR)
        table = self.content.find("table", id="tabResult")
        self.products = table.find_all("span", class_="txtTit")
        self.codes = table.find_all("span", class_="RCod")
        self.quantities = table.find_all("span", class_="Rqtd")
        self.uoms = table.find_all("span", class_="RUN")
        self.unitary_prices = table.find_all("span", class_="RvlUnit")

        return self._process_items()

    def _process_items(self) -> list[Item]:
        items: Dict[str, Item] = {}

        for i in range(len(self.products)):
            code = sanitize_text(self.codes[i].text)
            quantity = to_float(self.quantities[i].text)

            if code in items.keys():
                items[code].quantidade += quantity
                continue

            price = to_float(self.unitary_prices[i].text)
            uom = sanitize_text(self.uoms[i].text).upper()
            product_description = sanitize_text(self.products[i].text).upper()

            product = Produto(code, product_description)
            item = Item(
                product,
                quantity,
                price,
                uom,
            )

            items[code] = item

        return list(items.values())


class TotaisParser(Parser):
    CONTENT_SELECTOR = "conteudo"

    def parse(self, page) -> Totais:
        self.content = page.find("div", id=self.CONTENT_SELECTOR)
        totals = self._get_totals()
        return totals

    def _get_totals(self):
        totals = self.content.find_all("div", id="linhaTotal")
        payment_type = self.content.find_all("label", class_="tx")[0].text
        payment_type = sanitize_text(payment_type)

        values = self._get_totals_values(totals, payment_type)

        total_items = int(values.get("Qtd. total de itens:", 0))
        total_after_discount = values.get("Valor a pagar", 0)
        discounts = values.get("Descontos", 0)
        total_before_discount = values.get(
            "Valor total", total_after_discount - discounts
        )
        exchange = values.get("Troco", 0)

        return Totais(
            discounts,
            exchange,
            total_before_discount,
            total_after_discount,
            total_items,
            TipoPagamento.from_str(payment_type.upper()),
        )

    def _get_totals_values(self, totals: list, payment_type: str) -> dict:

        values = {}
        for total in totals:
            if total.find("label") is None:
                continue

            key = sanitize_text(total.find("label").string)

            if key == payment_type:
                continue
            key = "tax" if "Tributos Totais" in key else key.replace("R$:", "").strip()

            value = to_float(total.find("span").text)
            values[key] = value

        return values


class NfeParser(Parser):
    def __init__(self):
        self.parsers = {
            "empresa": EmpresaParser(),
            "informacoes": InformacoesNotaParser(),
            "itens": ItensParser(),
            "totais": TotaisParser(),
        }

    def parse(self, page) -> NotaFiscalEletronica:
        data = {}
        for name, parser in self.parsers.items():
            data[name] = parser.parse(page)

        return NotaFiscalEletronica(**data)
        # return NotaFiscalEletronica(**data)
