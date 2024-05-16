from typing import Any
from api.database import PostgresDatabase
from api.ports.repositories import Repository
from api.domain import Company, Address


class CompanyRepository(Repository):

    def __init__(self, client: PostgresDatabase):
        self.client = client

    def save(self, entity: Company) -> Company:
        with self.client as session:
            try:
                p = self.client.Company(
                    cnpj=entity.cnpj,
                    name=entity.name,
                    street=entity.address.street,
                    number=entity.address.number,
                    neighborhood=entity.address.neighborhood,
                    city=entity.address.city,
                    state=entity.address.state,
                    complement=entity.address.complement,
                    zip_code=entity.address.zip_code,
                )

                session.add(p)
                session.commit()

                return CompanyRepository.__to_entity(p)
            except Exception as e:
                session.rollback()
                raise e

    def delete(self, id: int) -> None:
        with self.client as session:
            try:
                session.query(self.client.Company).filter_by(id=id).delete()
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def find_by_id(self, id: int) -> Company:
        with self.client as session:
            company = session.query(self.client.Company).get(id)
            return CompanyRepository.__to_entity(company) if company else None

    def find_all(self, **filters) -> list[Company]:
        with self.client as session:
            companies = session.query(self.client.Company).filter_by(**filters).all()

            return (
                [CompanyRepository.__to_entity(company) for company in companies]
                if companies
                else []
            )

    def update(self, entity: Company) -> None:
        with self.client as session:
            try:
                company = session.query(self.client.Company).get(entity.id)
                company.cnpj = entity.cnpj
                company.name = entity.name
                company.street = entity.address.street
                company.number = entity.address.number
                company.neighborhood = entity.address.neighborhood
                company.city = entity.address.city
                company.state = entity.address.state
                company.complement = entity.address.complement
                company.zip_code = entity.address.zip_code
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    @staticmethod
    def __to_entity(company: Any):
        address = Address(
            street=company.street,
            number=company.number,
            neighborhood=company.neighborhood,
            city=company.city,
            state=company.state,
            complement=company.complement,
            zip_code=company.zip_code,
        )

        return Company(
            id=company.id, name=company.name, cnpj=company.cnpj, address=address
        )
