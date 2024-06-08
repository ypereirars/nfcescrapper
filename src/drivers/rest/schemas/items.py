from datetime import datetime
from pydantic import BaseModel


class ItemPatchRequestModel(BaseModel):
    quantity: float
    unit_price: float
    unity_of_measurement: str


class ItemPostRequestModel(ItemPatchRequestModel):
    product_id: int
    invoice_id: int


class ItemModel(ItemPostRequestModel):
    id: int
    product_code: str
    product_description: str
    created_on: datetime = datetime.now()
