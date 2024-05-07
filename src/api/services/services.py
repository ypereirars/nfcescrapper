from api.domain import Address, Company
from api.domain.entities.entities import EletronicInvoice
from api.domain.value_objects.value_objects import Taxes
from api.ports.services import Service
from api.domain import Product
from api.repositories.company import CompanyRepository
from api.repositories.invoice import InvoiceRepository
from api.repositories.product import ProductRepository
from api.routers.schema import CompanyInput, CompanyOutput, InvoiceModel


class ProductService(Service):

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def save(self, entity: Product) -> None:
        self.repository.save(entity)

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> Product:
        return self.repository.find_by_id(id)

    def find_all(self) -> list[Product]:
        return self.repository.find_all()

    def update(self, entity: Product) -> None:
        self.repository.update(entity)

    def find_by_code(self, code: str) -> Product:
        return self.repository.find_by_code(code)


class CompanyService(Service):

    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    def save(self, entity: CompanyInput) -> CompanyOutput:
        model = CompanyService.__from_basemodel(entity)
        entity = self.repository.save(model)
        return CompanyService.__to_basemodel(entity)

    def delete(self, id) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> CompanyOutput:
        entity = self.repository.find_by_id(id)

        return CompanyService.__to_basemodel(entity)

    def find_all(self) -> list[CompanyOutput]:
        entities = self.repository.find_all()

        return [CompanyService.__to_basemodel(entity) for entity in entities]

    def update(self, entity: CompanyInput) -> None:
        entity = self.__from_basemodel(entity)
        self.repository.update(entity)

    def find_by_cnpj(self, cnpj: str) -> CompanyOutput:
        entity = self.repository.find_by_cnpj(cnpj)

        return CompanyService.__to_basemodel(entity)

    @staticmethod
    def __from_basemodel(entity: CompanyInput) -> Company:
        address = Address(
            street=entity.street,
            number=entity.number,
            neighborhood=entity.neighborhood,
            city=entity.city,
            state=entity.state,
            complement=entity.complement,
            zip_code=entity.zip_code,
        )
        return Company(
            id=0,
            name=entity.name,
            cnpj=entity.cnpj,
            address=address,
        )

    @staticmethod
    def __to_basemodel(entity: Company) -> CompanyOutput:
        return CompanyOutput(
            id=entity.id,
            name=entity.name,
            cnpj=entity.cnpj,
            street=entity.address.street,
            number=entity.address.number,
            complement=entity.address.complement,
            neighborhood=entity.address.neighborhood,
            city=entity.address.city,
            state=entity.address.state,
            zip_code=entity.address.zip_code,
        )


class InvoiceService(Service):

    def __init__(self, repository: InvoiceRepository):
        self.repository = repository

    def save(self, entity: InvoiceModel) -> None:
        entity = InvoiceService.__from_basemodel(entity)
        self.repository.save(entity)

    def delete(self, id: int) -> None:
        self.repository.delete(id)

    def find_by_id(self, id: int) -> InvoiceModel:
        return self.repository.find_by_id(id)

    def find_all(self) -> list[InvoiceModel]:
        invoices = self.repository.find_all()

        return [InvoiceModel.from_entity(invoice) for invoice in invoices]

    def update(self, entity: InvoiceModel) -> None:
        entity = InvoiceService.__from_basemodel(entity)
        self.repository.update(entity)

    def find_by_access_key(self, access_key: str) -> InvoiceModel:
        return self.repository.find_by_access_key(access_key)

    @staticmethod
    def __from_basemodel(entity: InvoiceModel) -> EletronicInvoice:
        taxes = Taxes(
            federal=entity.federal_tax,
            state=entity.state_tax,
            municipal=entity.municipal_tax,
            source=entity.source,
        )

        company = Company(
            id=entity.company_id,
            cnpj=entity.cnpj,
            name=entity.company.name,
            address=Address(
                street=entity.company.street,
                number=entity.company.number,
                neighborhood=entity.company.neighborhood,
                city=entity.company.city,
                state=entity.company.state,
                complement=entity.company.complement,
                zip_code=entity.company.zip_code,
            ),
        )

        return EletronicInvoice(
            company=company,
            access_key=entity.access_key,
            number=entity.number,
            series=entity.series,
            issue_date=entity.issue_date,
            authorization_protocol=entity.authorization_protocol,
            authorization_date=entity.authorization_date,
            taxes=taxes,
        )
