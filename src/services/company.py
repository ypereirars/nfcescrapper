from typing import Any
from domain.entities.entities import (
    Company,
    Address,
)
from ports.services import Service
from repositories import (
    CompanyRepository,
)

from drivers.rest.schemas.companies import CompanyModel, CompanyPatchRequestModel

__all__ = ["CompanyService"]


class CompanyService(Service):

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def save(self, model: CompanyPatchRequestModel) -> CompanyModel:
        entity = self.repository.save(self.__from_model(model))
        return CompanyModel(**vars(entity))

    def delete(self, id) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> CompanyModel:
        entity = self.repository.find_by_id(id)

        return CompanyModel(**vars(entity)) if entity else None

    def find_all(self, **filters: dict[str, Any]) -> list[CompanyModel]:
        entities = self.repository.find_all(**filters)

        return [CompanyModel(**vars(entity)) for entity in entities]

    def get_by_cnpj(self, cnpj: str) -> CompanyModel:
        entity = self.repository.find_all(cnpj=cnpj)

        return CompanyModel(**vars(entity[0])) if entity else None

    def update(self, id: int, model: CompanyPatchRequestModel) -> None:
        self.repository.update(id, self.__from_model(model))

    def __from_model(self, model: CompanyPatchRequestModel):
        address = Address(
            street=model.street, number=model.number, city=model.city, state=model.state
        )
        company = Company(name=model.name, cnpj=model.cnpj, address=address)
        return company
