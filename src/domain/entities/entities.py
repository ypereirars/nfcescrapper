from dataclasses import dataclass
from datetime import datetime
from ..value_objects import Address, Taxes, Totals


@dataclass
class Entity:
    id: int = 0


@dataclass
class User(Entity):
    first_name: str = ""
    last_name: str = ""
    username: str = ""
    created_on: datetime = datetime.now()


@dataclass
class Company(Entity):
    name: str = ""
    cnpj: str = ""
    address: Address = None
    created_on: datetime = datetime.now()

    @property
    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "cnpj": self.cnpj,
            "created_on": self.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            **vars(self.address),
        }


@dataclass
class Product(Entity):
    def __init__(
        self,
        id: int = 0,
        code: str = "",
        description: str = "",
        created_on: datetime = datetime.now(),
    ) -> None:
        self.id = id
        self.code = code
        self.description = description
        self.created_on = created_on

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value):
        self.__code = f"{value:0>13}"

    def __str__(self):
        return f"{self.code:0>13} {self.description}"

    @property
    def __dict__(self):
        return {
            "id": self.id,
            "code": self.code,
            "description": self.description,
            "created_on": self.created_on.strftime("%Y-%m-%d %H:%M:%S"),
        }


@dataclass
class Item(Entity):
    invoice_id: int = 0
    product_id: int = 0
    product: Product = None
    quantity: int = 1
    unit_price: float = 0.0
    unity_of_measurement: str = "UN"
    created_on: datetime = datetime.now()

    @property
    def total_price(self) -> float:
        return self.unit_price * self.quantity

    @property
    def __dict__(self):
        product = vars(self.product) if self.product else {}
        id = product.pop("id")
        product["product_id"] = id

        return {
            **product,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "unity_of_measurement": self.unity_of_measurement,
            "total_price": self.total_price,
        }


@dataclass
class EletronicInvoice(Entity):
    user_id: int = 0
    user: User = None
    company_id: int = 0
    company: Company = None
    items: list[Item] = None
    totals: Totals = None
    taxes: Taxes = None
    access_key: str = ""
    number: str = ""
    series: str = ""
    issue_date: str = ""
    authorization_protocol: str = ""
    authorization_date: str = ""
    created_on: datetime = datetime.now()

    @property
    def __dict__(self):
        company = vars(self.company)
        id = company.pop("id")
        company["company_id"] = id

        return {
            "id": self.id,
            "access_key": self.access_key,
            "number": self.number,
            "series": self.series,
            "issue_date": self.issue_date,
            "authorization_protocol": self.authorization_protocol,
            "authorization_date": self.authorization_date,
            "user": vars(self.user) if self.user else {},
            "company": company,
            "items": [vars(item) for item in self.items] if self.items else [],
            "totals": vars(self.totals) if self.totals else {},
            "taxes": vars(self.taxes) if self.taxes else {},
            "created_on": self.created_on.strftime("%Y-%m-%d %H:%M:%S"),
        }
