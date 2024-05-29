from typing import Any
from domain.entities.entities import Company, Address, Product
from drivers.rest.schemas.products import ProductModel
from ports.services import Service
from repositories import (
    CompanyRepository,
    InvoiceRepository,
    ItemRepository,
    ProductRepository,
)
from drivers.rest.routers.schema import (
    InvoiceModel,
    ItemModel,
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
        entity = self.repository.save(model.to_entity())

        return InvoiceModel.from_entity(entity)

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> InvoiceModel:
        entity = self.repository.find_by_id(id)

        return InvoiceModel.from_entity(entity) if entity else None

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
        entity = self.repository.find_by_id(id)

        return ItemModel.from_entity(entity) if entity else None

    def find_all(self, **filters: dict[str, Any]) -> list[ItemModel]:
        entities = self.repository.find_all(**filters)

        return [ItemModel.from_entity(item) for item in entities]

    def update(self, model: ItemModel) -> None:
        self.repository.update(model.to_entity())
