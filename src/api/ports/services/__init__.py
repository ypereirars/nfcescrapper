from abc import ABC

from pydantic import BaseModel


class Service(ABC):

    def save(self, entity: BaseModel) -> None:
        pass

    def delete(self, entity: BaseModel) -> None:
        pass

    def find_by_id(self, id: int) -> BaseModel:
        pass

    def find_all(self) -> list[BaseModel]:
        pass

    def update(self, entity: BaseModel) -> None:
        pass
