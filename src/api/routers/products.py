from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from api.dependencies import get_products_services
from api.services import ProductService
from .schema import ProductModel
from api.domain import Product

__all__ = ["router"]

router = APIRouter(prefix="/products")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_products(
    repository: Annotated[ProductService, Depends(get_products_services)]
) -> list[ProductModel]:

    return repository.find_all()


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(
    product_id: int,
    repository: Annotated[ProductService, Depends(get_products_services)],
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

    product = repository.find_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    return product


@router.patch("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    product: ProductModel,
    repository: Annotated[ProductService, Depends(get_products_services)],
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

    repository.update(
        Product(id=product_id, code=product.code, description=product.description)
    )

    return product


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductModel,
    repository: Annotated[ProductService, Depends(get_products_services)],
) -> ProductModel:

    entity = product.to_entity(0)

    repository.save(entity)

    return ProductModel.from_entity(entity)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    repository: Annotated[ProductService, Depends(get_products_services)],
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

    repository.delete(product_id)


@router.get("/code/{code}", status_code=status.HTTP_200_OK)
async def get_product_by_code(
    code: str,
    repository: Annotated[ProductService, Depends(get_products_services)],
) -> None:
    product = repository.find_by_code(code)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    return product
