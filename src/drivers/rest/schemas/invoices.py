from datetime import datetime

from pydantic import BaseModel


class InvoicePatchRequestModel(BaseModel):
    access_key: str
    number: str
    series: str
    authorization_protocol: str
    authorization_date: datetime
    issue_date: datetime
    federal_tax: float
    state_tax: float
    municipal_tax: float
    source_tax: str


class InvoicePostRequestModel(InvoicePatchRequestModel):
    company_id: int
    user_id: int


class InvoiceModel(InvoicePostRequestModel):
    id: int

    created_on: datetime = datetime.now()
