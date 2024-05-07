from pydantic import BaseModel

from api.domain import Product, Company, Address


class ProductInput(BaseModel):
    code: str
    description: str

    def to_entity(self, id: int) -> Product:
        return Product(
            id=id,
            code=self.code,
            description=self.description,
        )


class ProductOutput(BaseModel):
    id: int
    code: str
    description: str

    @classmethod
    def from_entity(cls, product: Product) -> "ProductOutput":
        return cls(
            id=product.id,
            code=product.code,
            description=product.description,
        )


class CompanyInput(BaseModel):
    name: str
    cnpj: str
    street: str
    number: str
    complement: str
    neighborhood: str
    city: str
    state: str
    zip_code: str

    def to_entity(self, id: int) -> Company:
        address = Address(
            street=self.street,
            number=self.number,
            complement=self.complement,
            neighborhood=self.neighborhood,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
        )
        return Company(id=id, name=self.name, cnpj=self.cnpj, address=address)


class CompanyOutput(BaseModel):
    id: int
    name: str
    cnpj: str
    street: str
    number: str
    complement: str
    neighborhood: str
    city: str
    state: str
    zip_code: str

    @classmethod
    def from_entity(cls, company: Company) -> "CompanyOutput":
        return cls(
            id=company.id,
            name=company.name,
            cnpj=company.cnpj,
            street=company.address.street,
            number=company.address.number,
            complement=company.address.complement,
            neighborhood=company.address.neighborhood,
            city=company.address.city,
            state=company.address.state,
            zip_code=company.address.zip_code,
        )
