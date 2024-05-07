from abc import ABC
from api.domain import Entity


class Repository(ABC):

    def save(self, entity: Entity) -> Entity:
        pass

    def delete(self, id: int) -> None:
        pass

    def find_by_id(self, id: int) -> Entity:
        pass

    def find_all(self) -> list[Entity]:
        pass

    def update(self, entity: Entity) -> None:
        pass
