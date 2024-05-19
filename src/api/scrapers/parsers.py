import re
from datetime import datetime
from typing import Any
from .utils import to_float, sanitize_text, clean_text, remove_consecutive_spaces
from .interfaces import Parser, ContentParser, InfoParser

__all__ = [
    "AddressParser",
    "CompanyParser",
    "InformacoesNotaParser",
    "TaxParser",
    "ItemsParser",
    "TotalsParser",
    "NfceParser",
]


class AddressParser(ContentParser):
    def parse(self, page: Any) -> dict[str, Any]:
        content = self._get_content(page)
        info = content.find_all("div", class_="text")
        text = sanitize_text(info[1].text)
        address = text.upper().split(",")

        labels = [
            "logradouro",
            "numero",
            "complemento",
            "bairro",
            "municipio",
            "uf",
            "cep",
        ]

        try:
            result = {key: value for key, value in zip(labels, address)}
        except Exception:
            result = {label: "" for label in labels}
            result["logradouro"] = text.upper()
        finally:
            for label in labels:
                result[label] = "" if label not in result.keys() else result[label]

        return result


class CompanyParser(ContentParser):
    def parse(self, page) -> dict[str:Any]:
        content = self._get_content(page)

        info = content.find_all("div", class_="text")
        name = content.find_all("div", class_="txtTopo")[0].text

        result = {
            "cnpj": clean_text(info[0].text),
            "razao_social": sanitize_text(name).upper(),
        }

        return result


class InformacoesNotaParser(InfoParser):
    CONTENT_SELECTOR = "infos"

    def parse(self, page) -> dict:
        content = self._get_content(page)
        result = {
            "chave_acesso": clean_text(content.find("span", class_="chave").text),
            "numero": "",
            "serie": "",
            "data_emissao": "",
            "protocolo_autorizacao": "",
            "data_autorizacao": "",
        }
        DATE_FORMAT = "%d/%m/%Y %H:%M:%S%z"
        try:
            info_contents = content.find("ul", class_="ui-listview").find("li").contents
            info_contents = [
                info
                for info in info_contents
                if info != "\n" and info.name != "br" and info.name != "strong"
            ]

            date_str = "".join(info_contents[2].split("\n")[0].rsplit(":", 1))
            emission_date = datetime.strptime(date_str, DATE_FORMAT)

            authorization = (
                info_contents[3].replace("às", "").replace("\n", "").split(" ")
            )
            protocol = authorization[0]

            date_str = "".join(
                remove_consecutive_spaces(authorization[1:]).rsplit(":", 1)
            )
            authorization_date = datetime.strptime(date_str, DATE_FORMAT)

            result["numero"] = sanitize_text(info_contents[0])
            result["serie"] = sanitize_text(info_contents[1])
            result["data_emissao"] = emission_date
            result["protocolo_autorizacao"] = protocol
            result["data_autorizacao"] = authorization_date

        except Exception:
            pass

        return result


class TaxParser(InfoParser):
    def parse(self, page) -> dict:
        content = self._get_content(page)
        taxpayer_info = content.findAll("div")[-3].find("ul").text.strip()
        pattern = re.compile(
            r"trib *aprox: *R\$ *(\d+[.,]\d+) *fed *R\$ *(\d+[.,]\d+) *est *R\$ *(\d+[.,]\d+) *mun *fonte: *(\w+)",
            re.IGNORECASE,
        )
        matches = pattern.match(taxpayer_info)

        taxes = {
            "federal": 0.0,
            "estadual": 0.0,
            "municipal": 0.0,
            "fonte": "",
        }
        if not matches:
            attribute = content.parent.find("span", class_="totalNumb txtObs")
            tax = to_float(attribute.text) if attribute else 0.0
            taxes["federal"] = tax
        else:
            taxes["federal"] = to_float(matches.group(1))
            taxes["estadual"] = to_float(matches.group(2))
            taxes["municipal"] = to_float(matches.group(3))
            taxes["fonte"] = matches.group(4)

        return taxes


class ItemsParser(ContentParser):
    def parse(self, page) -> dict[str, Any]:
        content = self._get_content(page)
        items_table = content.find("table", id="tabResult")

        products = items_table.find_all("span", class_="txtTit")
        codes = items_table.find_all("span", class_="RCod")
        quantities = items_table.find_all("span", class_="Rqtd")
        uoms = items_table.find_all("span", class_="RUN")
        unitary_prices = items_table.find_all("span", class_="RvlUnit")

        columns = zip(products, codes, quantities, uoms, unitary_prices)

        return {"itens": self._get_items(columns)}

    def _get_items(self, columns):
        items = {}

        for product, code, quantity, uom, unitary_price in columns:
            code = sanitize_text(code.text)
            quantity = to_float(quantity.text)
            price = to_float(unitary_price.text)
            uom = sanitize_text(uom.text).upper()
            product_description = sanitize_text(product.text).upper()

            if code in items.keys():
                items[code]["quantidade"] += quantity
                continue

            items[code] = {
                "codigo_produto": code,
                "descricao_produto": product_description,
                "quantidade": quantity,
                "preco_unitario": price,
                "unidade_medida": uom,
            }

        return items


class TotalsParser(ContentParser):
    CONTENT_SELECTOR = "conteudo"

    def parse(self, page) -> dict[str, Any]:
        content = page.find("div", id=self.CONTENT_SELECTOR)
        payment_type = content.find_all("label", class_="tx")[0].text
        payment_type = sanitize_text(payment_type)

        totals = self.__get_totals(content, payment_type)
        values = self.__get_values(totals)

        return {
            "quantidade_itens": int(values.get("Qtd. total de itens:", 0)),
            "valor_a_pagar": to_float(values.get("Valor a pagar", 0.0)),
            "desconto": to_float(values.get("Descontos", 0.0)),
            "troco": to_float(values.get("Troco", 0.0)),
            "tipo_pagamento": payment_type.upper(),
        }

    def __get_totals(self, content: Any, payment_type: str) -> list:
        totals_line = content.find_all("div", id="linhaTotal")

        totals = []

        for total in totals_line:
            label = total.find("label")

            if label is None or sanitize_text(label.string) == payment_type:
                continue

            totals.append(total)

        return totals

    def __get_values(self, totals: list) -> dict:
        values = {"moeda": "R$"}
        for total in totals:
            label = sanitize_text(total.find("label").string)
            if label.lower().startswith("valor total"):
                values["moeda"] = label.split(" ")[-1].strip().upper()

            label = (
                "tax"
                if "Tributos Totais" in label
                else label.replace("R$:", "").strip()
            )

            values[label] = to_float(total.find("span").text)

        return values


class NfceParser(Parser):
    def __init__(self):
        self.parsers = {
            "endereco": AddressParser(),
            "empresa": CompanyParser(),
            "informacoes": InformacoesNotaParser(),
            "tributos": TaxParser(),
            "totais": TotalsParser(),
            "itens": ItemsParser(),
        }

    def parse(self, page) -> dict[str, Any]:
        data = {}
        for name, parser in self.parsers.items():
            try:
                if name == "itens":
                    items = parser.parse(page)
                    data[name] = items["itens"]
                else:
                    data[name] = {**parser.parse(page)}
            except Exception:
                data[name] = {}

        return data
