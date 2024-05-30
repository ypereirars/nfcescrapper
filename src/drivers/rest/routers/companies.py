from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from drivers.rest.dependencies import get_companies_services, validate_id_input
from services import CompanyService
from ..schemas.companies import CompanyModel, CompanyPatchRequestModel

__all__ = ["router"]

router = APIRouter(prefix="/companies")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_companies(
    service: Annotated[CompanyService, Depends(get_companies_services)]
) -> list[CompanyModel]:

    return service.find_all()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_company(
    id: Annotated[int, Depends(validate_id_input)],
    service: Annotated[CompanyService, Depends(get_companies_services)],
) -> None:

    company = service.find_by_id(id)

    return company


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_company(
    id: Annotated[int, Depends(validate_id_input)],
    company: CompanyPatchRequestModel,
    service: Annotated[CompanyService, Depends(get_companies_services)],
) -> None:

    service.update(id, company)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_company(
    company: CompanyPatchRequestModel,
    service: Annotated[CompanyService, Depends(get_companies_services)],
) -> CompanyModel:
    model = service.save(company)

    return model


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    id: Annotated[int, Depends(validate_id_input)],
    service: Annotated[CompanyService, Depends(get_companies_services)],
) -> None:
    """Delete a company by it's ID

    Args:
        id (int): The company ID
    """
    service.delete(id)


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

    company = service.get_by_cnpj(cnpj=cnpj)

    return company
