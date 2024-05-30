from typing import Any
from domain.entities.entities import User
from drivers.rest.schemas.users import (
    UserModel,
    UserPatchRequestModel,
    UserPostRequestModel,
)
from ports.services import Service
from repositories import UserRepository
from .exceptions import EntityAlreadyExists, EntityNotExists

__all__ = ["UserService"]


class UserService(Service):

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def save(self, model: UserPostRequestModel) -> UserModel:
        user = User(
            first_name=model.first_name,
            last_name=model.last_name,
            username=model.username,
        )
        _entity = self.find_by_username(user.username)

        if _entity:
            raise EntityAlreadyExists("Usuário")

        entity = self.repository.save(user)

        return UserModel(**vars(entity)) if entity else None

    def delete(self, id: int) -> None:
        user = self.repository.find_by_id(id)

        if user is None:
            raise EntityNotExists("Usuário")

        self.repository.delete(id)

    def find_by_id(self, id: int) -> UserModel:
        entity = self.repository.find_by_id(id)

        return UserModel(**vars(entity)) if entity else None

    def find_by_username(self, username: str) -> UserModel:
        entity = self.repository.find_all(username=username)

        return UserModel(**vars(entity[0])) if entity else None

    def find_all(self, **filters: dict[str, Any]) -> list[UserModel]:
        entities = self.repository.find_all(**filters)

        return [UserModel(**vars(entity)) for entity in entities]

    def update(self, id: int, model: UserPatchRequestModel) -> None:
        user = self.repository.find_by_id(id)

        if not user:
            raise EntityNotExists("Usuário")

        self.repository.update(id, User(**vars(model)))
