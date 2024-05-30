from typing import Any
from domain.entities.entities import (
    Company,
    EletronicInvoice,
    User,
)
from domain.value_objects.value_objects import Taxes
from drivers.rest.schemas.invoices import (
    InvoiceModel,
    InvoicePostRequestModel,
    InvoicePatchRequestModel,
)
from ports.services import Service
from repositories import InvoiceRepository

__all__ = ["InvoiceService"]


class InvoiceService(Service):

    def __init__(self, repository: InvoiceRepository):
        self.repository = repository

    def save(self, model: InvoiceModel) -> InvoiceModel:

        entity = self.repository.save(self.__from_model(model))

        return InvoiceModel(**vars(entity))

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> InvoiceModel:
        entity = self.repository.find_by_id(id)

        return (
            InvoiceModel(
                id=entity.id,
                company_id=entity.company_id,
                user_id=entity.user_id,
                access_key=entity.access_key,
                number=entity.number,
                series=entity.series,
                issue_date=entity.issue_date,
                authorization_protocol=entity.authorization_protocol,
                authorization_date=entity.authorization_date,
                federal_tax=entity.taxes.federal,
                state_tax=entity.taxes.state,
                municipal_tax=entity.taxes.municipal,
                source_tax=entity.taxes.source,
                created_on=entity.created_on,
            )
            if entity
            else None
        )

    def find_by_company(self, company_id: int) -> list[InvoiceModel]:
        entities = self.repository.find_all(company_id=company_id)

        return [
            InvoiceModel(
                id=entity.id,
                company_id=entity.company_id,
                user_id=entity.user_id,
                access_key=entity.access_key,
                number=entity.number,
                series=entity.series,
                issue_date=entity.issue_date,
                authorization_protocol=entity.authorization_protocol,
                authorization_date=entity.authorization_date,
                federal_tax=entity.taxes.federal,
                state_tax=entity.taxes.state,
                municipal_tax=entity.taxes.municipal,
                source_tax=entity.taxes.source,
                created_on=entity.created_on,
            )
            for entity in entities
        ]

    def find_by_user(self, user_id: int) -> list[InvoiceModel]:
        entities = self.repository.find_all(user_id=user_id)

        return [
            InvoiceModel(
                id=entity.id,
                company_id=entity.company_id,
                user_id=entity.user_id,
                access_key=entity.access_key,
                number=entity.number,
                series=entity.series,
                issue_date=entity.issue_date,
                authorization_protocol=entity.authorization_protocol,
                authorization_date=entity.authorization_date,
                federal_tax=entity.taxes.federal,
                state_tax=entity.taxes.state,
                municipal_tax=entity.taxes.municipal,
                source_tax=entity.taxes.source,
                created_on=entity.created_on,
            )
            for entity in entities
        ]

    def find_all(self, **filters: dict[str, Any]) -> list[InvoiceModel]:
        entities = self.repository.find_all(**filters)

        return [
            InvoiceModel(
                id=entity.id,
                company_id=entity.company_id,
                user_id=entity.user_id,
                access_key=entity.access_key,
                number=entity.number,
                series=entity.series,
                issue_date=entity.issue_date,
                authorization_protocol=entity.authorization_protocol,
                authorization_date=entity.authorization_date,
                federal_tax=entity.taxes.federal,
                state_tax=entity.taxes.state,
                municipal_tax=entity.taxes.municipal,
                source_tax=entity.taxes.source,
                created_on=entity.created_on,
            )
            for entity in entities
        ]

    def update(self, id: int, entity: InvoicePatchRequestModel) -> None:
        taxes = Taxes(
            federal=entity.federal_tax,
            state=entity.state_tax,
            municipal=entity.municipal_tax,
            source=entity.source_tax,
        )
        model = EletronicInvoice(
            id=id,
            access_key=entity.access_key,
            number=entity.number,
            series=entity.series,
            issue_date=entity.issue_date,
            authorization_protocol=entity.authorization_protocol,
            authorization_date=entity.authorization_date,
            taxes=taxes,
        )
        self.repository.update(id, model)

    def __from_model(self, model: InvoicePostRequestModel) -> EletronicInvoice:
        invoice = EletronicInvoice(
            user=User(model.user_id),
            company=Company(model.company_id),
            access_key=model.access_key,
            number=model.number,
            series=model.series,
            issue_date=model.issue_date,
            authorization_protocol=model.authorization_protocol,
            authorization_date=model.authorization_date,
            taxes=Taxes(
                federal=model.federal_tax,
                state=model.state_tax,
                municipal=model.municipal_tax,
                source=model.source_tax,
            ),
        )
        return invoice
