from typing import Any
from api.database import PostgresDatabase
from api.ports.repositories import Repository
from api.domain import Product


class ProductRepository(Repository):

    def __init__(self, client: PostgresDatabase):
        self.client = client

    def save(self, entity: Product) -> None:
        with self.client as session:
            try:
                p = self.client.Product(
                    code=entity.code, description=entity.description
                )

                session.add(p)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def delete(self, id: int) -> None:
        with self.client as session:
            try:
                session.query(self.client.Product).filter_by(id=id).delete()
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def find_by_id(self, id: int) -> Product:
        with self.client as session:
            product = session.query(self.client.Product).get(id)
            return ProductRepository.__to_entity(product) if product else None

    def find_all(self, **filters) -> list[Product]:
        with self.client as session:
            products = session.query(self.client.Product).filter_by(**filters).all()
            return (
                [ProductRepository.__to_entity(product) for product in products]
                if products
                else []
            )

    def update(self, entity: Product) -> None:
        with self.client as session:
            try:
                product = session.query(self.client.Product).get(entity.id)
                product.code = entity.code
                product.description = entity.description
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @staticmethod
    def __to_entity(product: Any):
        return Product(
            id=product.id, code=product.code, description=product.description
        )
