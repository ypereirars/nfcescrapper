from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from dependencies import get_invoices_services
from services import InvoiceService
from .schema import InvoiceModel

__all__ = ["router"]

router = APIRouter(prefix="/invoices")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_invoices(
    service: Annotated[InvoiceService, Depends(get_invoices_services)]
) -> list[InvoiceModel]:

    return service.find_all()


@router.get("/{invoice_id}", status_code=status.HTTP_200_OK)
async def get_invoice(
    invoice_id: int,
    service: Annotated[InvoiceService, Depends(get_invoices_services)],
) -> None:
    try:
        invoice_id = int(invoice_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da nota fiscal é obrigatório",
        )

    if invoice_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID da nota fiscal inválido"
        )

    invoice = service.find_by_id(invoice_id)

    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nota fiscal não encontrada"
        )

    return invoice


@router.patch("/{invoice_id}", status_code=status.HTTP_200_OK)
async def update_invoice(
    invoice_id: int,
    invoice: InvoiceModel,
    service: Annotated[InvoiceService, Depends(get_invoices_services)],
) -> None:
    try:
        invoice_id = int(invoice_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da nota fiscal é obrigatório",
        )

    if invoice_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID da nota fiscal inválido"
        )

    service.update(invoice)

    return invoice


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_invoice(
    invoice: InvoiceModel,
    service: Annotated[InvoiceService, Depends(get_invoices_services)],
) -> InvoiceModel:
    entity = service.save(invoice)

    return InvoiceModel.from_entity(entity)


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice(
    invoice_id: int,
    service: Annotated[InvoiceService, Depends(get_invoices_services)],
) -> None:
    """Delete a invoice by it's ID

    Args:
        invoice_id (int): The invoice ID
    """
    try:
        invoice_id = int(invoice_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da nota fiscal é obrigatório",
        )

    if invoice_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID da nota fiscal inválido"
        )

    service.delete(invoice_id)


@router.get("/company/{company_id}", status_code=status.HTTP_200_OK)
async def get_all_invoices_by_company(
    company_id: int, service: Annotated[InvoiceService, Depends(get_invoices_services)]
) -> list[InvoiceModel]:

    try:
        company_id = int(company_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da nota fiscal é obrigatório",
        )

    if company_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID da nota fiscal inválido"
        )

    return service.find_all(company_id=company_id)
