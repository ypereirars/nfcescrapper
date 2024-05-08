from abc import ABC
from typing import Any
from api.domain import Entity


class Repository(ABC):

    def save(self, entity: Entity) -> Entity:
        pass

    def delete(self, id: int) -> None:
        pass

    def find_by_id(self, id: int) -> Entity:
        pass

    def find_all(self, **filters: dict[str, Any]) -> list[Entity]:
        pass

    def update(self, entity: Entity) -> None:
        pass
