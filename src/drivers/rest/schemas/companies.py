from datetime import datetime
from pydantic import BaseModel


class CompanyPatchRequestModel(BaseModel):
    name: str
    cnpj: str
    street: str
    number: str
    complement: str
    neighborhood: str
    city: str
    state: str
    zip_code: str


class CompanyModel(CompanyPatchRequestModel):
    id: int
    created_on: datetime = datetime.now()
