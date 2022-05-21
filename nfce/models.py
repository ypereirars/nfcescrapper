from datetime import datetime


class Company(object):
    def __init__(self, name: str, cnpj: str, address: str) -> None:
        self.name = name
        self.cnpj = cnpj
        self.address = address

    def __str__(self) -> str:
        return f"{self.name} - {self.cnpj} - {self.address}"


class Product(object):

    def __init__(self,
                 code,
                 name,
                 price,
                 quantity=1,
                 currency='R$',
                 unity_of_measure='UN',
                 total_price=None) -> None:
        self.code = code
        self.name = name
        self.price = price
        self.quantity = quantity
        self.currency = currency
        self.unity_of_measure = unity_of_measure
        self.total_price = self.price * self.quantity if total_price is None else total_price

    def __str__(self):
        return f'{self.code} - {self.name} - {self.currency}{self.price} - {self.quantity}{self.unity_of_measure} - {self.currency}{self.total_price}'


class PaymentTotals(object):

    def __init__(self,
                 exchange,
                 tax,
                 payment_type,
                 total_before_discount,
                 total_after_discount,
                 total_items,
                 discounts) -> None:
        self.exchange = exchange
        self.tax = tax
        self.payment_type = payment_type
        self.total_before_discount = total_before_discount
        self.total_after_discount = total_after_discount
        self.total_items = total_items
        self.discounts = discounts


class EletronicInvoice(object):

    def __init__(self, company, items, totals, access_key, number, serie, issue_date) -> None:
        self.company = company
        self.items = items
        self.totals = totals
        self.access_key = access_key
        self.number = number
        self.serie = serie
        self.issue_date = issue_date

    def serialize(self) -> dict:
        return {
            'access_key': self.access_key,
            'number': self.number,
            'serie': self.serie,
            'issue_date': '' if self.issue_date == '' else datetime.strftime(self.issue_date, '%Y-%m-%d %H:%M:%S%z'),
            'company': vars(self.company),
            'items': [vars(item) for item in self.items],
            'totals': vars(self.totals)
        }

    def to_csv(self) -> list:
        company = vars(self.company).values()
        totals = vars(self.totals).values()
        header = [*vars(self.company).keys(), *vars(self.totals).keys(),
                  'code', 'name', 'quantity', 'unity_of_measure', 'price', 'currency', 'total_price',
                  'access_key', 'number', 'serie', 'issue_date']

        for item in self.items:
            yield (header, [*company, *totals, item.code, item.name, item.quantity,
                            item.unity_of_measure, item.price, item.currency, item.total_price,
                            self.access_key, self.number, self.serie, self.issue_date])
