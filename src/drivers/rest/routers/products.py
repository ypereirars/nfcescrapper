from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from drivers.rest.dependencies import get_products_services
from drivers.rest.schemas.products import ProductModel, ProductPatchRequestModel
from services import ProductService

__all__ = ["router"]

router = APIRouter(prefix="/products")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_products(
    service: Annotated[ProductService, Depends(get_products_services)]
) -> list[ProductModel]:
    return service.find_all()


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(
    product_id: int,
    service: Annotated[ProductService, Depends(get_products_services)],
) -> None:
    try:
        product_id = int(product_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID do produto é obrigatório",
        )

    if product_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID do produto inválido"
        )

    product = service.find_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    return product


@router.patch("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    product: ProductPatchRequestModel,
    service: Annotated[ProductService, Depends(get_products_services)],
) -> None:
    try:
        product_id = int(product_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID do produto é obrigatório",
        )

    if product_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID do produto inválido"
        )

    service.update(product_id, product)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductPatchRequestModel,
    service: Annotated[ProductService, Depends(get_products_services)],
) -> ProductModel:

    model = service.save(product)

    return model


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    service: Annotated[ProductService, Depends(get_products_services)],
) -> None:
    """Delete a product by it's ID

    Args:
        product_id (int): The product ID
    """
    try:
        product_id = int(product_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID do produto é obrigatório",
        )

    if product_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID do produto inválido"
        )

    service.delete(product_id)


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

    print(">>", products)

    if products is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    return products
