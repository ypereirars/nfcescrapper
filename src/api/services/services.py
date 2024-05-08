from typing import Any
from api.ports.services import Service
from api.repositories import (
    CompanyRepository,
    InvoiceRepository,
    ItemRepository,
    ProductRepository,
)
from api.routers.schema import CompanyModel, InvoiceModel, ItemModel, ProductModel

__all__ = ["ProductService", "CompanyService", "InvoiceService", "ItemService"]


class ProductService(Service):

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def save(self, entity: ProductModel) -> None:
        self.repository.save(entity)

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> ProductModel:
        return self.repository.find_by_id(id)

    def find_all(self, **filters: dict[str, Any]) -> list[ProductModel]:
        return self.repository.find_all()

    def update(self, entity: ProductModel) -> None:
        self.repository.update(entity)

    def find_by_code(self, code: str) -> ProductModel:
        return self.repository.find_by_code(code)


class CompanyService(Service):

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def save(self, entity: CompanyModel) -> CompanyModel:
        entity = self.repository.save(entity.to_entity())
        return CompanyModel.from_entity(entity)

    def delete(self, id) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> CompanyModel:
        entity = self.repository.find_by_id(id)

        return CompanyModel.from_entity(entity)

    def find_all(self, **filters: dict[str, Any]) -> list[CompanyModel]:
        entities = self.repository.find_all()

        return [CompanyModel.from_entity(entity) for entity in entities]

    def update(self, entity: CompanyModel) -> None:
        self.repository.update(entity.to_entity())

    def find_by_cnpj(self, cnpj: str) -> CompanyModel:
        entity = self.repository.find_by_cnpj(cnpj)

        return CompanyModel.from_entity(entity)


class InvoiceService(Service):

    def __init__(self, repository: InvoiceRepository):
        self.repository = repository

    def save(self, entity: InvoiceModel) -> None:
        entity = InvoiceService.__from_basemodel(entity)
        self.repository.save(entity)

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> InvoiceModel:
        return self.repository.find_by_id(id)

    def find_all(self, **filters: dict[str, Any]) -> list[InvoiceModel]:
        invoices = self.repository.find_all(**filters)

        return [InvoiceModel.from_entity(invoice) for invoice in invoices]

    def update(self, entity: InvoiceModel) -> None:
        self.repository.update(entity.to_entity())

    def find_by_access_key(self, access_key: str) -> InvoiceModel:
        return self.repository.find_by_access_key(access_key)


class ItemService(Service):

    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def save(self, entity: ItemModel) -> ItemModel:
        self.repository.save(entity.to_entity())

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> ItemModel:
        item = self.repository.find_by_id(id)
        return ItemModel.from_entity(item)

    def find_all(self, **filters: dict[str, Any]) -> list[ItemModel]:
        items = self.repository.find_all(**filters)
        return [ItemModel.from_entity(item) for item in items]

    def update(self, entity: ItemModel) -> None:
        self.repository.update(entity)
