from datetime import datetime
from pydantic import BaseModel


class ProductPatchRequestModel(BaseModel):
    code: str
    description: str


class ProductModel(ProductPatchRequestModel):
    id: int
    created_on: datetime = datetime.now()
