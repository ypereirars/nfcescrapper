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
    __entity_name__ = "Usuário"

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def save(self, model: UserPostRequestModel) -> UserModel:
        try:
            _entity = self.find_by_username(model.username)
        except EntityNotExists:
            _entity = None

        if _entity:
            raise EntityAlreadyExists(self.__entity_name__)

        user = User(
            first_name=model.first_name,
            last_name=model.last_name,
            username=model.username,
        )

        entity = self.repository.save(user)

        return UserModel(**vars(entity))

    def delete(self, id: int) -> None:
        self.find_by_id(id)

        self.repository.delete(id)

    def find_by_id(self, id: int) -> UserModel:
        entity = self.repository.find_by_id(id)

        if entity is None:
            raise EntityNotExists(self.__entity_name__)

        return UserModel(**vars(entity))

    def find_by_username(self, username: str) -> UserModel:
        entity = self.repository.find_all(username=username)

        if entity is None or len(entity) == 0:
            raise EntityNotExists(self.__entity_name__)

        return UserModel(**vars(entity[0]))

    def find_all(self, **filters: dict[str, Any]) -> list[UserModel]:
        entities = self.repository.find_all(**filters)

        return [UserModel(**vars(entity)) for entity in entities]

    def update(self, id: int, model: UserPatchRequestModel) -> None:
        self.find_by_id(id)

        self.repository.update(id, User(**vars(model)))
