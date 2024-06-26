from typing import Annotated

from fastapi import APIRouter, Depends, status

from drivers.rest.dependencies import get_invoices_services, validate_id_input
from drivers.rest.schemas.invoices import (
    InvoiceModel,
    InvoicePatchRequestModel,
    InvoicePostRequestModel,
)
from services import InvoiceService

__all__ = ["router"]

router = APIRouter(prefix="/invoices")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_invoices(
    service: Annotated[InvoiceService, Depends(get_invoices_services)]
) -> list[InvoiceModel]:

    return service.find_all()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_invoice(
    id: Annotated[int, Depends(validate_id_input)],
    service: Annotated[InvoiceService, Depends(get_invoices_services)],
) -> None:

    invoice = service.find_by_id(id)

    return invoice


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_invoice(
    id: Annotated[int, Depends(validate_id_input)],
    invoice: InvoicePatchRequestModel,
    service: Annotated[InvoiceService, Depends(get_invoices_services)],
) -> None:

    service.update(id, invoice)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_invoice(
    invoice: InvoicePostRequestModel,
    service: Annotated[InvoiceService, Depends(get_invoices_services)],
) -> InvoiceModel:
    entity = service.save(invoice)

    return InvoiceModel.from_entity(entity)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice(
    id: Annotated[int, Depends(validate_id_input)],
    service: Annotated[InvoiceService, Depends(get_invoices_services)],
) -> None:
    """Delete a invoice by it's ID

    Args:
        id (int): The invoice ID
    """

    service.delete(id)


@router.get("/companies/{id}", status_code=status.HTTP_200_OK)
async def get_all_invoices_by_company(
    id: Annotated[int, Depends(validate_id_input)],
    service: Annotated[InvoiceService, Depends(get_invoices_services)],
) -> list[InvoiceModel]:

    return service.find_by_company(id)


@router.get("/users/{id}", status_code=status.HTTP_200_OK)
async def get_all_invoices_by_user(
    id: Annotated[int, Depends(validate_id_input)],
    service: Annotated[InvoiceService, Depends(get_invoices_services)],
) -> list[InvoiceModel]:

    return service.find_by_user(id)
