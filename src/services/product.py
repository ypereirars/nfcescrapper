from typing import Any
from domain.entities.entities import Product
from drivers.rest.schemas.products import ProductModel
from ports.services import Service
from repositories import ProductRepository

__all__ = ["ProductService"]


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
