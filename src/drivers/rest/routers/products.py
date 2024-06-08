from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from drivers.rest.dependencies import get_products_services, validate_id_input
from drivers.rest.schemas.products import ProductModel, ProductPatchRequestModel
from services import ProductService

__all__ = ["router"]

router = APIRouter(prefix="/products")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_products(
    service: Annotated[ProductService, Depends(get_products_services)]
) -> list[ProductModel]:
    return service.find_all()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_product(
    id: Annotated[int, Depends(validate_id_input)],
    service: Annotated[ProductService, Depends(get_products_services)],
) -> None:
    product = service.find_by_id(id)

    return product


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_product(
    id: Annotated[int, Depends(validate_id_input)],
    product: ProductPatchRequestModel,
    service: Annotated[ProductService, Depends(get_products_services)],
) -> None:

    service.update(id, product)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductPatchRequestModel,
    service: Annotated[ProductService, Depends(get_products_services)],
) -> ProductModel:

    model = service.save(product)

    return model


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    id: Annotated[int, Depends(validate_id_input)],
    service: Annotated[ProductService, Depends(get_products_services)],
) -> None:
    """Delete a product by it's ID

    Args:
        id (int): The product ID
    """

    service.delete(id)


@router.get("/code/{code}", status_code=status.HTTP_200_OK)
async def get_product_by_code(
    code: str,
    service: Annotated[ProductService, Depends(get_products_services)],
) -> ProductModel:

    if code == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código do produto é obrigatório",
        )

    products = service.find_by_code(code=code)

    return products
