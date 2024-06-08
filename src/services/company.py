from typing import Any
from domain.entities.entities import Company, Address
from ports.services import Service
from repositories import CompanyRepository

from drivers.rest.schemas.companies import CompanyModel, CompanyPatchRequestModel
from services.exceptions import EntityAlreadyExists, EntityNotExists

__all__ = ["CompanyService"]


class CompanyService(Service):
    __entity_name__ = "Empresa"

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def save(self, model: CompanyPatchRequestModel) -> CompanyModel:
        companies = self.find_all(cnpj=model.cnpj)
        if len(companies) > 0:
            raise EntityAlreadyExists(self.__entity_name__)

        entity = self.repository.save(self.__from_model(model))
        return CompanyModel(**vars(entity))

    def delete(self, id: int) -> None:
        self.find_by_id(id)
        self.repository.delete(id)

    def find_by_id(self, id: int) -> CompanyModel:
        entity = self.repository.find_by_id(id)

        return CompanyModel(**vars(entity))

    def find_all(self, **filters: dict[str, Any]) -> list[CompanyModel]:
        entities = self.repository.find_all(**filters)

        return [CompanyModel(**vars(entity)) for entity in entities]

    def get_by_cnpj(self, cnpj: str) -> CompanyModel:
        entity = self.repository.find_all(cnpj=cnpj)

        if entity is None or len(entity) == 0:
            raise EntityNotExists(self.__entity_name__)

        return CompanyModel(**vars(entity[0]))

    def update(self, id: int, model: CompanyPatchRequestModel) -> None:
        self.find_by_id(id)

        self.repository.update(id, self.__from_model(model))

    def __from_model(self, model: CompanyPatchRequestModel):
        address = Address(
            street=model.street, number=model.number, city=model.city, state=model.state
        )
        company = Company(name=model.name, cnpj=model.cnpj, address=address)
        return company
