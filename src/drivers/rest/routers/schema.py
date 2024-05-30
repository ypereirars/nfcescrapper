from pydantic import BaseModel
from domain import Product, Item

__all__ = ["ItemModel"]


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
        product = Product(
            id=self.product_id,
            code=self.product_code,
            description=self.product_description,
        )
        return Item(
            product_id=self.product_id,
            invoice_id=self.invoice_id,
            quantity=self.quantity,
            unit_price=self.unit_price,
            unity_of_measurement=self.unity_of_measurement,
            product=product,
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
