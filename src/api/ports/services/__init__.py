from abc import ABC
from typing import Any

from pydantic import BaseModel

__all__ = ["Service"]


class Service(ABC):

    def save(self, entity: BaseModel) -> None:
        pass

    def delete(self, entity: BaseModel) -> None:
        pass

    def find_by_id(self, id: int) -> BaseModel:
        pass

    def find_all(self, **filters: dict[str, Any]) -> list[BaseModel]:
        pass

    def update(self, entity: BaseModel) -> None:
        pass
