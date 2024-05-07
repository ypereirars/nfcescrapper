from pydantic import BaseModel

from api.domain import Product


class ProductInput(BaseModel):
    code: str
    description: str

    def to_entity(self, id: int) -> Product:
        return Product(
            id=id,
            code=self.code,
            description=self.description,
        )


class ProductOutput(BaseModel):
    id: int
    code: str
    description: str

    @classmethod
    def from_entity(cls, product: Product) -> "ProductOutput":
        return cls(
            id=product.id,
            code=product.code,
            description=product.description,
        )
