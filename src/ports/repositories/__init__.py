from abc import ABC
from typing import Any
from domain import Entity

__all__ = ["Repository"]


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
