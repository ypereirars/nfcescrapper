from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from drivers.rest.dependencies import get_companies_services
from services import CompanyService
from .schema import CompanyModel

__all__ = ["router"]

router = APIRouter(prefix="/companies")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_companies(
    service: Annotated[CompanyService, Depends(get_companies_services)]
) -> list[CompanyModel]:

    return service.find_all()


@router.get("/{company_id}", status_code=status.HTTP_200_OK)
async def get_company(
    company_id: int,
    service: Annotated[CompanyService, Depends(get_companies_services)],
) -> None:
    try:
        company_id = int(company_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da empresa é obrigatório",
        )

    if company_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID da empresa inválido"
        )

    company = service.find_by_id(company_id)

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada"
        )

    return company


@router.patch("/{company_id}", status_code=status.HTTP_200_OK)
async def update_company(
    company_id: int,
    company: CompanyModel,
    service: Annotated[CompanyService, Depends(get_companies_services)],
) -> None:
    try:
        company_id = int(company_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da empresa é obrigatório",
        )

    if company_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID da empresa inválido"
        )

    service.update(company)

    return company


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_company(
    company: CompanyModel,
    service: Annotated[CompanyService, Depends(get_companies_services)],
) -> CompanyModel:
    entity = service.save(company)

    return CompanyModel.from_entity(entity)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: int,
    service: Annotated[CompanyService, Depends(get_companies_services)],
) -> None:
    """Delete a company by it's ID

    Args:
        company_id (int): The company ID
    """
    try:
        company_id = int(company_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID da empresa é obrigatório",
        )

    if company_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID da empresa inválido"
        )

    service.delete(company_id)


@router.get("/cnpj/{cnpj}", status_code=status.HTTP_200_OK)
async def get_company_by_cnpj(
    cnpj: str,
    service: Annotated[CompanyService, Depends(get_companies_services)],
) -> None:

    if cnpj == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CNPJ da empresa é obrigatório",
        )

    company = service.find_all(cnpj=cnpj)

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada"
        )

    return company
