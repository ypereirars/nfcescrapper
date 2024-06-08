from sqlalchemy.orm import Session
from ports.repositories import Repository
from domain import Company, Address
from database.schema import CompanySchema


class CompanyRepository(Repository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, entity: Company) -> Company:
        company = CompanySchema(
            cnpj=entity.cnpj,
            name=entity.name,
            street=entity.address.street,
            number=entity.address.number,
            neighborhood=entity.address.neighborhood,
            city=entity.address.city,
            state=entity.address.state,
            complement=entity.address.complement,
            zip_code=entity.address.zip_code,
            created_on=entity.created_on,
        )

        try:
            self.session.add(company)
            self.session.commit()
            self.session.refresh(company)

            return CompanyRepository.__to_entity(company)
        except Exception as ex:
            self.session.rollback()
            raise ex

    def delete(self, id: int) -> None:
        try:
            self.session.query(CompanySchema).filter_by(id=id).delete()
            self.session.commit()
            self.session.flush()
        except Exception as ex:
            self.session.rollback()
            raise ex

    def find_by_id(self, id: int) -> Company:
        company = self.session.query(CompanySchema).get(id)

        return CompanyRepository.__to_entity(company) if company else None

    def find_all(self, **filters) -> list[Company]:
        companies = self.session.query(CompanySchema).filter_by(**filters).all()

        return (
            [CompanyRepository.__to_entity(company) for company in companies]
            if companies
            else []
        )

    def update(self, id: int, company: Company) -> None:
        company = CompanySchema(
            id=id,
            cnpj=company.cnpj,
            name=company.name,
            street=company.address.street,
            number=company.address.number,
            neighborhood=company.address.neighborhood,
            city=company.address.city,
            state=company.address.state,
            complement=company.address.complement,
            zip_code=company.address.zip_code,
            created_on=company.created_on,
        )
        try:
            self.session.merge(company)
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise ex

    @staticmethod
    def __to_entity(company: CompanySchema):
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
            id=company.id,
            name=company.name,
            cnpj=company.cnpj,
            address=address,
            created_on=company.created_on,
        )
