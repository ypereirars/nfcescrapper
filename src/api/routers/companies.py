from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from api.dependencies import get_companies_services
from api.services.services import CompanyService
from .schema import CompanyInput, CompanyOutput
from api.domain import Company

router = APIRouter(prefix="/companies")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_companies(
    service: Annotated[CompanyService, Depends(get_companies_services)]
) -> list[CompanyOutput]:

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
    company: CompanyInput,
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
    company: CompanyInput,
    service: Annotated[CompanyService, Depends(get_companies_services)],
) -> CompanyOutput:
    entity = service.save(company)

    return CompanyOutput.from_entity(entity)


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


@router.get("/code/{code}", status_code=status.HTTP_200_OK)
async def get_company_by_cnpj(
    code: str,
    service: Annotated[CompanyService, Depends(get_companies_services)],
) -> None:
    company = service.find_by_cnpj(code)

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada"
        )

    return company
