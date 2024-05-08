from api.database.schema import PostgresDatabase
from api.database.schema import Item as ItemDatabase
from api.domain.entities.entities import Item, Product
from api.ports.repositories import Repository


class ItemRepository(Repository):
    def __init__(self, client: PostgresDatabase):
        self.client = client

    def save(self, entity: Item) -> Item:
        with self.client as session:
            try:
                invoice = self.client.Item(
                    product_id=entity.product.id,
                    invoice_id=entity.invoice_id,
                    quantity=entity.quantity,
                    unit_price=entity.unit_price,
                    unity_of_measurement=entity.unity_of_measurement,
                )

                session.add(invoice)
                session.commit()

                return ItemRepository.__to_entity(invoice)
            except Exception as e:
                session.rollback()
                raise e

    def delete(self, id: int) -> None:
        with self.client as session:
            try:
                invoice = session.query(self.client.Item).filter_by(id=id).first()
                session.delete(invoice)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def find_by_id(self, id: int) -> Item:
        with self.client as session:
            item = session.query(self.client.Item).filter_by(id=id).first()
            return ItemRepository.__to_entity(item)

    def find_all(self, filters: dict = {}) -> list[Item]:
        with self.client as session:
            items = session.query(self.client.Item).filter_by(**filters).all()
            return [ItemRepository.__to_entity(item) for item in items]

    def update(self, entity: Item) -> None:
        with self.client as session:
            try:
                item = session.query(self.client.Item).filter_by(id=entity.id).first()
                item.product_id = entity.product_id
                item.invoice_id = entity.invoice_id
                item.quantity = entity.quantity
                item.unit_price = entity.unit_price
                item.unity_of_measurement = entity.unity_of_measurement

                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @staticmethod
    def __to_entity(item: ItemDatabase):
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
