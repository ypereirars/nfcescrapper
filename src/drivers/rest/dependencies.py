from typing import Annotated
from fastapi import Depends
from settings.database import get_db_connection
from sqlalchemy.orm import Session
from repositories import (
    CompanyRepository,
    ItemRepository,
    ProductRepository,
    InvoiceRepository,
)
from services import (
    CompanyService,
    ItemService,
    ProductService,
    InvoiceService,
)
from ports.services import Service

from dotenv import load_dotenv

load_dotenv()


__all__ = [
    "get_products_repository",
    "get_companies_repository",
    "get_invoices_repository",
    "get_items_repository",
    "get_products_services",
    "get_companies_services",
    "get_invoices_services",
    "get_items_services",
]


# Repositories


def get_products_repository(
    postgres_client: Session = Depends(get_db_connection),
) -> Session:
    return ProductRepository(postgres_client)


def get_companies_repository(
    postgres_client: Session = Depends(get_db_connection),
) -> Session:
    return CompanyRepository(postgres_client)


def get_invoices_repository(
    postgres_client: Session = Depends(get_db_connection),
) -> Session:
    return InvoiceRepository(postgres_client)


def get_items_repository(
    postgres_client: Session = Depends(get_db_connection),
) -> Session:
    return ItemRepository(postgres_client)


# Services


def get_products_services(
    repository: Annotated[ProductRepository, Depends(get_products_repository)],
) -> Service:
    return ProductService(repository)


def get_companies_services(
    repository: Annotated[CompanyRepository, Depends(get_companies_repository)],
) -> Service:
    return CompanyService(repository)


def get_invoices_services(
    repository: Annotated[InvoiceRepository, Depends(get_invoices_repository)],
) -> Service:
    return InvoiceService(repository)


def get_items_services(
    repository: Annotated[ItemRepository, Depends(get_items_repository)],
) -> Service:
    return ItemService(repository)
