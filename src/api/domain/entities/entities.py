from dataclasses import dataclass
from ..value_objects import Address, Taxes, Totals


@dataclass
class Entity:
    id: int = 0


@dataclass
class User(Entity):
    first_name: str = ""
    last_name: str = ""
    username: str = ""


@dataclass
class Company(Entity):
    name: str = ""
    cnpj: str = ""
    address: Address

    @property
    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "cnpj": self.cnpj,
            **vars(self.address),
        }


@dataclass
class Product(Entity):
    code: str = ""
    description: str = ""


@dataclass
class Item(Entity):
    product: Product
    quantity: int = 1
    unit_price: float = 0.0
    uom: str = "UN"

    @property
    def total_price(self) -> float:
        return self.unit_price * self.quantity

    @property
    def __dict__(self):
        product = vars(self.product)
        id = product.pop("id")
        product["product_id"] = id

        return {
            **vars(product),
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "uom": self.uom,
            "total_price": self.total_price,
        }


@dataclass
class EletronicInvoice(Entity):
    access_key: str = ""
    number: str = ""
    series: str = ""
    issue_date: str = ""
    authorization_protocol: str = ""
    authorization_date: str = ""
    company: Company
    items: list[Item]
    totals: Totals
    taxes: Taxes

    @property
    def __dict__(self):
        company = vars(self.company)
        id = company.pop("id")
        company["company_id"] = id

        return {
            "company": company,
            "items": [vars(item) for item in self.items],
            "totals": vars(self.totals),
            "taxes": vars(self.taxes),
        }
