from typing import Any
from database.schema import ItemSchema
from domain import Item, Product
from ports.repositories import Repository
from sqlalchemy.orm import Session


class ItemRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, entity: Item) -> Item:
        invoice = ItemSchema(
            product_id=entity.product_id,
            invoice_id=entity.invoice_id,
            quantity=entity.quantity,
            unit_price=entity.unit_price,
            unity_of_measurement=entity.unity_of_measurement,
        )

        self.session.add(invoice)
        self.session.commit()
        self.session.refresh(invoice)

    def delete(self, id: int) -> None:
        self.session.query(ItemSchema).filter_by(id=id).delete()
        self.session.commit()

    def find_by_id(self, id: int) -> Item:
        item = self.session.query(ItemSchema).filter_by(id=id).first()
        return ItemRepository.__to_entity(item) if item else None

    def find_all(self, **filters: dict[str, Any]) -> list[Item]:
        items = self.session.query(ItemSchema).filter_by(**filters).all()
        return [ItemRepository.__to_entity(item) for item in items]

    def update(self, id: int, entity: Item) -> None:
        item = ItemSchema(
            id=id,
            quantity=entity.quantity,
            unit_price=entity.unit_price,
            unity_of_measurement=entity.unity_of_measurement,
        )
        self.session.merge(item)
        self.session.commit()

    @staticmethod
    def __to_entity(item: Any) -> Item:
        product = Product(item.product_id, item.product.code, item.product.description)
        return Item(
            id=item.id,
            invoice_id=item.invoice_id,
            product_id=item.product_id,
            product=product,
            quantity=item.quantity,
            unit_price=item.unit_price,
            unity_of_measurement=item.unity_of_measurement,
        )
