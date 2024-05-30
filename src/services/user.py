from typing import Any
from domain.entities.entities import User
from drivers.rest.schemas.users import UserModel, UserPatchRequestModel
from ports.services import Service
from repositories import UserRepository

__all__ = ["UserService"]


class UserService(Service):

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def save(self, model: UserModel) -> UserModel:
        entity = self.repository.save(User(**vars(model)))
        return UserModel(**vars(entity))

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> UserModel:
        entity = self.repository.find_by_id(id)

        return UserModel(**vars(entity)) if entity else None

    def find_all(self, **filters: dict[str, Any]) -> list[UserModel]:
        entities = self.repository.find_all(**filters)

        return [UserModel(**vars(entity)) for entity in entities]

    def update(self, id: int, model: UserPatchRequestModel) -> None:
        self.repository.update(id, User(**vars(model)))
