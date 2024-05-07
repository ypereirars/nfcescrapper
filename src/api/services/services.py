from typing import Any
from api.database.schema import PostgresDatabase
from api.ports.services import Service
from api.domain import Product
from api.repositories.product import ProductRepository


class ProductService(Service):

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def save(self, entity: Product) -> None:
        self.repository.save(entity)

    def delete(self, entity: Product) -> None:
        self.repository.delete(entity)

    def find_by_id(self, id: int) -> Product:
        return self.repository.find_by_id(id)

    def find_all(self) -> list[Product]:
        return self.repository.find_all()

    def update(self, entity: Product) -> None:
        self.repository.update(entity)

    def find_by_code(self, code: str) -> Product:
        return self.repository.find_by_code(code)
