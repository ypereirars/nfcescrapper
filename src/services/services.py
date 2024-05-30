from typing import Any
from domain.entities.entities import (
    Company,
    Address,
    EletronicInvoice,
    Item,
    Product,
    User,
)
from domain.value_objects.value_objects import Taxes
from drivers.rest.schemas.invoices import (
    InvoiceModel,
    InvoicePostRequestModel,
    InvoicePatchRequestModel,
)
from drivers.rest.schemas.items import ItemModel, ItemPostRequestModel
from drivers.rest.schemas.products import ProductModel
from ports.services import Service
from repositories import (
    CompanyRepository,
    InvoiceRepository,
    ItemRepository,
    ProductRepository,
)

from drivers.rest.schemas.companies import CompanyModel, CompanyPatchRequestModel

__all__ = ["ProductService", "CompanyService", "InvoiceService", "ItemService"]


class ProductService(Service):

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def save(self, model: ProductModel) -> ProductModel:
        entity = self.repository.save(Product(**vars(model)))
        return ProductModel(**vars(entity))

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> ProductModel:
        entity = self.repository.find_by_id(id)

        return ProductModel(**vars(entity)) if entity else None

    def find_all(self, **filters: dict[str, Any]) -> list[ProductModel]:
        entities = self.repository.find_all(**filters)

        return [ProductModel(**vars(entity)) for entity in entities]

    def find_by_code(self, code: str) -> ProductModel:
        entity = self.repository.find_all(code=code)

        return ProductModel(**vars(entity[0])) if entity else None

    def update(self, id: int, model: ProductModel) -> None:
        self.repository.update(id, Product(**vars(model)))


class CompanyService(Service):

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def save(self, model: CompanyPatchRequestModel) -> CompanyModel:
        entity = self.repository.save(self.__from_model(model))
        return CompanyModel(**vars(entity))

    def delete(self, id) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> CompanyModel:
        entity = self.repository.find_by_id(id)

        return CompanyModel(**vars(entity)) if entity else None

    def find_all(self, **filters: dict[str, Any]) -> list[CompanyModel]:
        entities = self.repository.find_all(**filters)

        return [CompanyModel(**vars(entity)) for entity in entities]

    def get_by_cnpj(self, cnpj: str) -> CompanyModel:
        entity = self.repository.find_all(cnpj=cnpj)

        return CompanyModel(**vars(entity[0])) if entity else None

    def update(self, id: int, model: CompanyPatchRequestModel) -> None:
        self.repository.update(id, self.__from_model(model))

    def __from_model(self, model: CompanyPatchRequestModel):
        address = Address(
            street=model.street, number=model.number, city=model.city, state=model.state
        )
        company = Company(name=model.name, cnpj=model.cnpj, address=address)
        return company


class InvoiceService(Service):

    def __init__(self, repository: InvoiceRepository):
        self.repository = repository

    def save(self, model: InvoiceModel) -> InvoiceModel:

        entity = self.repository.save(self.__from_model(model))

        return InvoiceModel(**vars(entity))

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> InvoiceModel:
        entity = self.repository.find_by_id(id)

        return (
            InvoiceModel(
                id=entity.id,
                company_id=entity.company_id,
                user_id=entity.user_id,
                access_key=entity.access_key,
                number=entity.number,
                series=entity.series,
                issue_date=entity.issue_date,
                authorization_protocol=entity.authorization_protocol,
                authorization_date=entity.authorization_date,
                federal_tax=entity.taxes.federal,
                state_tax=entity.taxes.state,
                municipal_tax=entity.taxes.municipal,
                source_tax=entity.taxes.source,
                created_on=entity.created_on,
            )
            if entity
            else None
        )

    def find_by_company(self, company_id: int) -> list[InvoiceModel]:
        entities = self.repository.find_all(company_id=company_id)

        return [
            InvoiceModel(
                id=entity.id,
                company_id=entity.company_id,
                user_id=entity.user_id,
                access_key=entity.access_key,
                number=entity.number,
                series=entity.series,
                issue_date=entity.issue_date,
                authorization_protocol=entity.authorization_protocol,
                authorization_date=entity.authorization_date,
                federal_tax=entity.taxes.federal,
                state_tax=entity.taxes.state,
                municipal_tax=entity.taxes.municipal,
                source_tax=entity.taxes.source,
                created_on=entity.created_on,
            )
            for entity in entities
        ]

    def find_by_user(self, user_id: int) -> list[InvoiceModel]:
        entities = self.repository.find_all(user_id=user_id)

        return [
            InvoiceModel(
                id=entity.id,
                company_id=entity.company_id,
                user_id=entity.user_id,
                access_key=entity.access_key,
                number=entity.number,
                series=entity.series,
                issue_date=entity.issue_date,
                authorization_protocol=entity.authorization_protocol,
                authorization_date=entity.authorization_date,
                federal_tax=entity.taxes.federal,
                state_tax=entity.taxes.state,
                municipal_tax=entity.taxes.municipal,
                source_tax=entity.taxes.source,
                created_on=entity.created_on,
            )
            for entity in entities
        ]

    def find_all(self, **filters: dict[str, Any]) -> list[InvoiceModel]:
        entities = self.repository.find_all(**filters)

        return [
            InvoiceModel(
                id=entity.id,
                company_id=entity.company_id,
                user_id=entity.user_id,
                access_key=entity.access_key,
                number=entity.number,
                series=entity.series,
                issue_date=entity.issue_date,
                authorization_protocol=entity.authorization_protocol,
                authorization_date=entity.authorization_date,
                federal_tax=entity.taxes.federal,
                state_tax=entity.taxes.state,
                municipal_tax=entity.taxes.municipal,
                source_tax=entity.taxes.source,
                created_on=entity.created_on,
            )
            for entity in entities
        ]

    def update(self, id: int, entity: InvoicePatchRequestModel) -> None:
        taxes = Taxes(
            federal=entity.federal_tax,
            state=entity.state_tax,
            municipal=entity.municipal_tax,
            source=entity.source_tax,
        )
        model = EletronicInvoice(
            id=id,
            access_key=entity.access_key,
            number=entity.number,
            series=entity.series,
            issue_date=entity.issue_date,
            authorization_protocol=entity.authorization_protocol,
            authorization_date=entity.authorization_date,
            taxes=taxes,
        )
        self.repository.update(id, model)

    def __from_model(self, model: InvoicePostRequestModel) -> EletronicInvoice:
        invoice = EletronicInvoice(
            user=User(model.user_id),
            company=Company(model.company_id),
            access_key=model.access_key,
            number=model.number,
            series=model.series,
            issue_date=model.issue_date,
            authorization_protocol=model.authorization_protocol,
            authorization_date=model.authorization_date,
            taxes=Taxes(
                federal=model.federal_tax,
                state=model.state_tax,
                municipal=model.municipal_tax,
                source=model.source_tax,
            ),
        )
        return invoice


class ItemService(Service):

    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def save(self, model: ItemPostRequestModel) -> ItemModel:
        entity = self.repository.save(Item(**vars(model)))

        return ItemModel(**vars(entity))

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> ItemModel:
        entity = self.repository.find_by_id(id)

        return self.__to_model(entity) if entity else None

    def find_by_invoice_id(self, invoice_id: int) -> list[ItemModel]:
        entities = self.repository.find_all(invoice_id=invoice_id)

        return [self.__to_model(item) for item in entities]

    def find_all(self, **filters: dict[str, Any]) -> list[ItemModel]:
        entities = self.repository.find_all(**filters)

        return [self.__to_model(item) for item in entities]

    def update(self, id: int, model: ItemModel) -> None:
        item = Item(
            id=id,
            quantity=model.quantity,
            unit_price=model.unit_price,
            unity_of_measurement=model.unity_of_measurement,
        )
        self.repository.update(id, item)

    def __to_model(self, entity: Item) -> ItemModel:
        return ItemModel(
            id=entity.id,
            invoice_id=entity.invoice_id,
            product_id=entity.product_id,
            product_code=entity.product.code,
            product_description=entity.product.description,
            quantity=entity.quantity,
            unit_price=entity.unit_price,
            unity_of_measurement=entity.unity_of_measurement,
            created_on=entity.created_on,
        )
