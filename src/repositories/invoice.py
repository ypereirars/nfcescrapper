from typing import Any
from database.schema import InvoiceSchema
from domain import EletronicInvoice, Taxes
from ports.repositories import Repository
from sqlalchemy.orm import Session


class InvoiceRepository(Repository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, entity: EletronicInvoice) -> EletronicInvoice:
        # TODO: If the invoice already exists, raise exception

        invoice = InvoiceSchema(
            user_id=entity.user.id,
            company_id=entity.company.id,
            access_key=entity.access_key,
            number=entity.number,
            series=entity.series,
            issue_date=entity.issue_date,
            authorization_protocol=entity.authorization_protocol,
            authorization_date=entity.authorization_date,
            federal_tax=entity.taxes.federal,
            state_tax=entity.taxes.state,
            city_tax=entity.taxes.municipal,
            source=entity.taxes.source,
        )
        try:
            self.session.add(invoice)
            self.session.commit()
            self.session.refresh(invoice)

            return InvoiceRepository.__to_entity(invoice)
        except Exception as ex:
            self.session.rollback()
            raise ex

    def delete(self, id: int) -> None:
        try:
            self.session.query(InvoiceSchema).filter_by(id=id).delete()
            self.session.commit()
            self.session.flush()
        except Exception as ex:
            self.session.rollback()
            raise ex

    def find_by_id(self, id: int) -> EletronicInvoice:
        invoice = self.session.query(InvoiceSchema).filter_by(id=id).first()
        return InvoiceRepository.__to_entity(invoice) if invoice else None

    def find_all(self, **filters: dict[str, Any]) -> list[EletronicInvoice]:
        invoices = self.session.query(InvoiceSchema).filter_by(**filters).all()
        return [InvoiceRepository.__to_entity(invoice) for invoice in invoices]

    def update(self, id: int, entity: EletronicInvoice) -> None:
        invoice = InvoiceSchema(
            id=id,
            access_key=entity.access_key,
            number=entity.number,
            series=entity.series,
            issue_date=entity.issue_date,
            authorization_protocol=entity.authorization_protocol,
            authorization_date=entity.authorization_date,
            federal_tax=entity.taxes.federal,
            state_tax=entity.taxes.state,
            city_tax=entity.taxes.municipal,
            source=entity.taxes.source,
        )
        try:
            self.session.merge(invoice)
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise ex

    @staticmethod
    def __to_entity(invoice: InvoiceSchema) -> EletronicInvoice:

        taxes = Taxes(
            federal=invoice.federal_tax,
            state=invoice.state_tax,
            municipal=invoice.city_tax,
            source=invoice.source,
        )

        return EletronicInvoice(
            id=invoice.id,
            access_key=invoice.access_key,
            number=invoice.number,
            series=invoice.series,
            issue_date=invoice.issue_date,
            authorization_protocol=invoice.authorization_protocol,
            authorization_date=invoice.authorization_date,
            company_id=invoice.company_id,
            user_id=invoice.user_id,
            taxes=taxes,
            items=[],
            totals=[],
        )
