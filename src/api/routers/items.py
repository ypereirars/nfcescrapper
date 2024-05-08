from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from api.dependencies import get_items_services
from api.services.services import ItemService
from .schema import ItemModel

router = APIRouter(prefix="/items")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_items(
    service: Annotated[ItemService, Depends(get_items_services)]
) -> list[ItemModel]:

    return service.find_all()


@router.get("/{item_id}", status_code=status.HTTP_200_OK)
async def get_item(
    item_id: int,
    service: Annotated[ItemService, Depends(get_items_services)],
) -> None:
    try:
        item_id = int(item_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da empresa é obrigatório",
        )

    if item_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID da empresa inválido"
        )

    item = service.find_by_id(item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada"
        )

    return item


@router.patch("/{item_id}", status_code=status.HTTP_200_OK)
async def update_item(
    item_id: int,
    item: ItemModel,
    service: Annotated[ItemService, Depends(get_items_services)],
) -> None:
    try:
        item_id = int(item_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da empresa é obrigatório",
        )

    if item_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID da empresa inválido"
        )

    service.update(item)

    return item


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemModel,
    service: Annotated[ItemService, Depends(get_items_services)],
) -> ItemModel:
    entity = service.save(item)

    return ItemModel.from_entity(entity)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    service: Annotated[ItemService, Depends(get_items_services)],
) -> None:
    """Delete a item by it's ID

    Args:
        item_id (int): The item ID
    """
    try:
        item_id = int(item_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID do item é obrigatório",
        )

    if item_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID do item inválido"
        )

    service.delete(item_id)


@router.get("/invoice/{invoice_id}", status_code=status.HTTP_200_OK)
async def get_by_invoice_id(
    invoice_id: int,
    service: Annotated[ItemService, Depends(get_items_services)],
) -> list[ItemModel]:
    try:
        invoice_id = int(invoice_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da nota é obrigatório",
        )
    if invoice_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID da nota fiscal inválido"
        )

    return service.find_all(invoice_id)
