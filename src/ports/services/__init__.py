from abc import ABC
from typing import Any

from pydantic import BaseModel

__all__ = ["Service"]


class Service(ABC):

    def save(self, model: BaseModel) -> BaseModel:
        pass

    def delete(self, id: int) -> None:
        pass

    def find_by_id(self, id: int) -> BaseModel:
        pass

    def find_all(self, **filters: dict[str, Any]) -> list[BaseModel]:
        pass

    def update(self, model: BaseModel) -> None:
        pass
