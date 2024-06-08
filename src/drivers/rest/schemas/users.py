from datetime import datetime
from pydantic import BaseModel


class UserPatchRequestModel(BaseModel):
    first_name: str
    last_name: str


class UserPostRequestModel(UserPatchRequestModel):
    username: str


class UserModel(UserPostRequestModel):
    id: int
    created_on: datetime = datetime.now()
