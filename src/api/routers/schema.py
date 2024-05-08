from pydantic import BaseModel
from datetime import datetime
from api.domain import Product, Company, Address, EletronicInvoice, Item

__all__ = ["ProductModel", "CompanyModel", "ItemModel", "InvoiceModel"]


class ProductModel(BaseModel):
    id: int
    code: str
    description: str

    def to_entity(self, id: int) -> Product:
        return Product(
            id=id,
            code=self.code,
            description=self.description,
        )

    @classmethod
    def from_entity(cls, product: Product) -> "ProductModel":
        return cls(
            id=product.id,
            code=product.code,
            description=product.description,
        )


class CompanyModel(BaseModel):
    id: int
    name: str
    cnpj: str
    street: str
    number: str
    complement: str
    neighborhood: str
    city: str
    state: str
    zip_code: str

    def to_entity(self, id: int) -> Company:
        address = Address(
            street=self.street,
            number=self.number,
            complement=self.complement,
            neighborhood=self.neighborhood,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
        )
        return Company(id=id, name=self.name, cnpj=self.cnpj, address=address)

    @classmethod
    def from_entity(cls, company: Company) -> "CompanyModel":
        return cls(
            id=company.id,
            name=company.name,
            cnpj=company.cnpj,
            street=company.address.street,
            number=company.address.number,
            complement=company.address.complement,
            neighborhood=company.address.neighborhood,
            city=company.address.city,
            state=company.address.state,
            zip_code=company.address.zip_code,
        )


class ItemModel(BaseModel):
    id: int
    product_id: int
    product_code: str
    product_description: str
    invoice_id: int
    quantity: float
    unit_price: float
    unity_of_measurement: str

    def to_entity(self) -> Item:
        return Item(
            product_id=self.product_id,
            invoice_id=self.invoice_id,
            quantity=self.quantity,
            unit_price=self.unit_price,
            unity_of_measurement=self.unity_of_measurement,
        )

    @classmethod
    def from_entity(cls, item: Item) -> "ItemModel":
        return cls(
            id=item.id,
            product_id=item.id,
            invoice_id=item.invoice_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            unity_of_measurement=item.unity_of_measurement,
            product_code=item.product.code,
            product_description=item.product.description,
        )


class InvoiceModel(BaseModel):
    id: int
    access_key: str
    number: str
    series: str
    authorization_protocol: str
    authorization_date: datetime
    issue_date: datetime
    federal_tax: float
    state_tax: float
    municipal_tax: float
    source: str
    company_id: int
    company: CompanyOutput
    items: list[ItemModel]

    def to_entity(self) -> Item:
        return EletronicInvoice(
            company_id=self.company_id,
            access_key=self.access_key,
            number=self.number,
            series=self.series,
            authorization_protocol=self.authorization_protocol,
            authorization_date=self.authorization_date,
            issue_date=self.issue_date,
            federal_tax=self.federal_tax,
            state_tax=self.state_tax,
            municipal_tax=self.municipal_tax,
            source=self.source,
        )

    @classmethod
    def from_entity(cls, invoice: EletronicInvoice) -> "InvoiceModel":
        company = CompanyOutput.from_entity(invoice.company)

        return cls(
            id=invoice.id,
            company=company,
            access_key=invoice.access_key,
            number=invoice.number,
            series=invoice.series,
            authorization_protocol=invoice.authorization_protocol,
            authorization_date=invoice.authorization_date,
            issue_date=invoice.issue_date,
            federal_tax=invoice.taxes.federal,
            state_tax=invoice.taxes.state,
            municipal_tax=invoice.taxes.municipal,
            source=invoice.taxes.source,
            company_id=invoice.company.id,
            items=[ItemModel.from_entity(item) for item in invoice.items],
        )
