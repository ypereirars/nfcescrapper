from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from drivers.rest.dependencies import get_users_services
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
    service: Annotated[UserService, Depends(get_users_services)]
) -> list[UserModel]:
    return service.find_all()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(
    id: int,
    service: Annotated[UserService, Depends(get_users_services)],
) -> None:
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID do usuário é obrigatório",
        )

    if id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário inválido"
        )

    user = service.find_by_id(id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    return user


@router.get("/{username}", status_code=status.HTTP_200_OK)
async def get_user_by_username(
    username: str,
    service: Annotated[UserService, Depends(get_users_services)],
) -> None:
    user = service.find_by_username(username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    return user


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_user(
    id: int,
    user: UserPatchRequestModel,
    service: Annotated[UserService, Depends(get_users_services)],
) -> None:
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID do usuário é obrigatório",
        )

    if id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário inválido"
        )

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
    id: int,
    service: Annotated[UserService, Depends(get_users_services)],
) -> None:
    """Delete a user by it's ID

    Args:
        id (int): The user ID
    """
    try:
        id = int(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID do usuário é obrigatório",
        )

    if id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário inválido"
        )

    service.delete(id)
