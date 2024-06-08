from sqlalchemy.orm import Session
from database.schema import ProductSchema
from ports.repositories import Repository
from domain import Product


class ProductRepository(Repository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, entity: Product) -> Product:
        product = ProductSchema(code=entity.code, description=entity.description)

        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)

        return Product(
            id=product.id, code=product.code, description=product.description
        )

    def delete(self, id: int) -> None:
        self.session.query(ProductSchema).filter_by(id=id).delete()
        self.session.commit()
        self.session.flush()

    def find_by_id(self, id: int) -> Product:
        product = self.session.query(ProductSchema).get(id)
        return self.__to_entity(product) if product else None

    def find_all(self, **filters) -> list[Product]:
        products = self.session.query(ProductSchema).filter_by(**filters).all()

        return (
            [ProductRepository.__to_entity(product) for product in products]
            if products
            else []
        )

    def update(self, id: int, entity: Product) -> None:
        product = ProductSchema(id=id, code=entity.code, description=entity.description)
        self.session.merge(product)
        self.session.commit()

    @staticmethod
    def __to_entity(product: ProductSchema) -> Product:
        return Product(
            id=product.id,
            code=product.code,
            description=product.description,
            created_on=product.created_on,
        )
