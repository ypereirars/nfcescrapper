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

    def save(self, model: ProductModel) -> ProductModel:
        entity = self.repository.save(model.to_entity())
        return ProductModel.from_entity(entity)

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> ProductModel:
        entity = self.repository.find_by_id(id)

        return ProductModel.from_entity(entity)

    def find_all(self, **filters: dict[str, Any]) -> list[ProductModel]:
        entities = self.repository.find_all(**filters)

        return [ProductModel.from_entity(entity) for entity in entities]

    def update(self, model: ProductModel) -> None:
        self.repository.update(model.to_entity())


class CompanyService(Service):

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def save(self, model: CompanyModel) -> CompanyModel:
        entity = self.repository.save(model.to_entity())
        return CompanyModel.from_entity(entity)

    def delete(self, id) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> CompanyModel:
        entity = self.repository.find_by_id(id)

        return CompanyModel.from_entity(entity)

    def find_all(self, **filters: dict[str, Any]) -> list[CompanyModel]:
        entities = self.repository.find_all(**filters)

        return [CompanyModel.from_entity(entity) for entity in entities]

    def update(self, model: CompanyModel) -> None:
        self.repository.update(model.to_entity())


class InvoiceService(Service):

    def __init__(self, repository: InvoiceRepository):
        self.repository = repository

    def save(self, model: InvoiceModel) -> InvoiceModel:
        entity = self.repository.save(model.to_entity())

        return InvoiceModel.from_entity(entity)

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> InvoiceModel:
        entity = self.repository.find_by_id(id)

        return InvoiceModel.from_entity(entity)

    def find_all(self, **filters: dict[str, Any]) -> list[InvoiceModel]:
        entities = self.repository.find_all(**filters)

        return [InvoiceModel.from_entity(entity) for entity in entities]

    def update(self, entity: InvoiceModel) -> None:
        self.repository.update(entity.to_entity())


class ItemService(Service):

    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def save(self, model: ItemModel) -> ItemModel:
        entity = self.repository.save(model.to_entity())

        return ItemModel.from_entity(entity)

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> ItemModel:
        item = self.repository.find_by_id(id)

        return ItemModel.from_entity(item)

    def find_all(self, **filters: dict[str, Any]) -> list[ItemModel]:
        entities = self.repository.find_all(**filters)

        return [ItemModel.from_entity(item) for item in entities]

    def update(self, model: ItemModel) -> None:
        self.repository.update(model.to_entity())
