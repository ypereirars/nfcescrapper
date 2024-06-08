from typing import Annotated

from fastapi import APIRouter, Depends, status

from drivers.rest.dependencies import get_items_services, validate_id_input
from drivers.rest.schemas.items import (
    ItemModel,
    ItemPatchRequestModel,
    ItemPostRequestModel,
)
from services import ItemService

__all__ = ["router"]

router = APIRouter(prefix="/items")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_items(
    service: Annotated[ItemService, Depends(get_items_services)]
) -> list[ItemModel]:

    return service.find_all()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_item(
    id: Annotated[int, Depends(validate_id_input)],
    service: Annotated[ItemService, Depends(get_items_services)],
) -> None:

    item = service.find_by_id(id)

    return item


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_item(
    id: Annotated[int, Depends(validate_id_input)],
    item: ItemPatchRequestModel,
    service: Annotated[ItemService, Depends(get_items_services)],
) -> None:

    service.update(id, item)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemPostRequestModel,
    service: Annotated[ItemService, Depends(get_items_services)],
) -> ItemModel:
    entity = service.save(item)

    return entity


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    id: Annotated[int, Depends(validate_id_input)],
    service: Annotated[ItemService, Depends(get_items_services)],
) -> None:
    """Delete a item by it's ID

    Args:
        id (int): The item ID
    """

    service.delete(id)


@router.get("/invoices/{id}", status_code=status.HTTP_200_OK)
async def get_by_invoice_id(
    id: Annotated[int, Depends(validate_id_input)],
    service: Annotated[ItemService, Depends(get_items_services)],
) -> list[ItemModel]:

    return service.find_all(invoice_id=id)
