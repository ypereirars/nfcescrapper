from typing import Any
from api.database import PostgresDatabase
from api.domain import EletronicInvoice, Company, Taxes, Address
from api.ports.repositories import Repository


class InvoiceRepository(Repository):

    def __init__(self, client: PostgresDatabase):
        self.client = client

    def save(self, entity: EletronicInvoice) -> EletronicInvoice:
        with self.client as session:
            try:
                p = self.client.Invoice(
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

                session.add(p)
                session.commit()

                return InvoiceRepository.__to_entity(p)
            except Exception as e:
                session.rollback()
                raise e

    def delete(self, id: int) -> None:
        with self.client as session:
            try:
                p = session.query(self.client.Invoice).filter_by(id=id).first()
                session.delete(p)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def find_by_id(self, id: int) -> EletronicInvoice:
        with self.client as session:
            invoice = session.query(self.client.Invoice).filter_by(id=id).first()
            return InvoiceRepository.__to_entity(invoice)

    def find_all(self, **filters: dict[str, Any]) -> list[EletronicInvoice]:
        with self.client as session:
            invoices = session.query(self.client.Invoice).filter_by(**filters).all()
            return [InvoiceRepository.__to_entity(invoice) for invoice in invoices]

    def update(self, entity: EletronicInvoice) -> None:
        with self.client as session:
            try:
                invoice = (
                    session.query(self.client.Invoice).filter_by(id=entity.id).first()
                )
                invoice.company_id = entity.company.id
                invoice.access_key = entity.access_key
                invoice.number = entity.number
                invoice.series = entity.series
                invoice.issue_date = entity.issue_date
                invoice.authorization_protocol = entity.authorization_protocol
                invoice.authorization_date = entity.authorization_date
                invoice.federal_tax = entity.taxes.federal
                invoice.state_tax = entity.taxes.state
                invoice.city_tax = entity.taxes.municipal
                invoice.source = entity.taxes.source

                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @staticmethod
    def __to_entity(invoice: Any) -> EletronicInvoice:
        taxes = Taxes(
            federal=invoice.federal_tax,
            state=invoice.state_tax,
            municipal=invoice.city_tax,
            source=invoice.source,
        )

        company = Company(
            id=invoice.company.id,
            cnpj=invoice.company.cnpj,
            name=invoice.company.name,
            address=Address(
                street=invoice.company.street,
                number=invoice.company.number,
                neighborhood=invoice.company.neighborhood,
                city=invoice.company.city,
                state=invoice.company.state,
                complement=invoice.company.complement,
                zip_code=invoice.company.zip_code,
            ),
        )

        return EletronicInvoice(
            id=invoice.id,
            company=company,
            access_key=invoice.access_key,
            number=invoice.number,
            series=invoice.series,
            issue_date=invoice.issue_date,
            authorization_protocol=invoice.authorization_protocol,
            authorization_date=invoice.authorization_date,
            taxes=taxes,
            items=invoice.items,
            totals=[],
        )
