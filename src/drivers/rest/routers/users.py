from typing import Annotated

from fastapi import APIRouter, Depends, status

from drivers.rest.dependencies import get_users_services, validate_id_input
from drivers.rest.schemas.users import (
    UserModel,
    UserPatchRequestModel,
    UserPostRequestModel,
)
from services import UserService

__all__ = ["router"]

router = APIRouter(prefix="/users")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(
    username: str, service: Annotated[UserService, Depends(get_users_services)]
) -> list[UserModel] | UserModel:

    if username:
        user = service.find_by_username(username)

        return user

    return service.find_all()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(
    id: int,
    service: Annotated[UserService, Depends(get_users_services)],
) -> UserModel:
    user = service.find_by_id(id)

    return user


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_user(
    id: Annotated[int, Depends(validate_id_input)],
    user: UserPatchRequestModel,
    service: Annotated[UserService, Depends(get_users_services)],
) -> None:
    service.update(id, user)

    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserPostRequestModel,
    service: Annotated[UserService, Depends(get_users_services)],
) -> UserModel:
    model = service.save(user)
    return model


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: Annotated[int, Depends(validate_id_input)],
    service: Annotated[UserService, Depends(get_users_services)],
) -> None:
    """Delete a user by it's ID

    Args:
        id (int): The user ID
    """

    service.delete(id)
