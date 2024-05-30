from typing import Any
from domain.entities.entities import Item
from drivers.rest.schemas.items import ItemModel, ItemPostRequestModel
from ports.services import Service
from repositories import ItemRepository

__all__ = ["ItemService"]


class ItemService(Service):

    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def save(self, model: ItemPostRequestModel) -> ItemModel:
        entity = self.repository.save(Item(**vars(model)))

        return ItemModel(**vars(entity))

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> ItemModel:
        entity = self.repository.find_by_id(id)

        return self.__to_model(entity) if entity else None

    def find_by_invoice_id(self, invoice_id: int) -> list[ItemModel]:
        entities = self.repository.find_all(invoice_id=invoice_id)

        return [self.__to_model(item) for item in entities]

    def find_all(self, **filters: dict[str, Any]) -> list[ItemModel]:
        entities = self.repository.find_all(**filters)

        return [self.__to_model(item) for item in entities]

    def update(self, id: int, model: ItemModel) -> None:
        item = Item(
            id=id,
            quantity=model.quantity,
            unit_price=model.unit_price,
            unity_of_measurement=model.unity_of_measurement,
        )
        self.repository.update(id, item)

    def __to_model(self, entity: Item) -> ItemModel:
        return ItemModel(
            id=entity.id,
            invoice_id=entity.invoice_id,
            product_id=entity.product_id,
            product_code=entity.product.code,
            product_description=entity.product.description,
            quantity=entity.quantity,
            unit_price=entity.unit_price,
            unity_of_measurement=entity.unity_of_measurement,
            created_on=entity.created_on,
        )
