from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from api.dependencies import get_products_repository
from api.repositories.repositories import ProductRepository
from .schema import ProductInput, ProductOutput
from api.domain import Product

router = APIRouter(prefix="/products")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_products(
    repository: Annotated[ProductRepository, Depends(get_products_repository)]
) -> list[ProductOutput]:

    return repository.find_all()


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(
    product_id: int,
    repository: Annotated[ProductRepository, Depends(get_products_repository)],
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
    product: ProductInput,
    repository: Annotated[ProductRepository, Depends(get_products_repository)],
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
    product: ProductInput,
    repository: Annotated[ProductRepository, Depends(get_products_repository)],
) -> ProductOutput:

    entity = product.to_entity(0)

    repository.save(entity)

    return ProductOutput.from_entity(entity)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    repository: Annotated[ProductRepository, Depends(get_products_repository)],
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

    repository.delete(Product(id=product_id))


@router.get("/code/{code}", status_code=status.HTTP_200_OK)
async def get_product_by_code(
    code: str,
    repository: Annotated[ProductRepository, Depends(get_products_repository)],
) -> None:
    product = repository.find_by_code(code)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    return product
