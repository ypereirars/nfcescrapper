from functools import lru_cache
from typing import Annotated
from fastapi import Depends
import os

from api.repositories.company import CompanyRepository
from api.repositories.item import ItemRepository
from .database.schema import PostgresDatabase
from .repositories.product import ProductRepository
from .services.services import (
    CompanyService,
    ItemService,
    ProductService,
    InvoiceService,
)
from .repositories.invoice import InvoiceRepository
from .ports.services import Service

from dotenv import load_dotenv

load_dotenv()


__all__ = [
    "get_postgres_client",
    "get_products_repository",
    "get_companies_repository",
    "get_invoices_repository",
    "get_items_repository",
    "get_products_services",
    "get_companies_services",
    "get_invoices_services",
    "get_items_services",
]


@lru_cache
def get_postgres_client() -> PostgresDatabase:
    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")

    if all([database, user, password, host]):
        return PostgresDatabase(database, user, password, host=host)

    raise ValueError("Missing environment variables for Postgres connection")


# Repositories


def get_products_repository(
    postgres_client: PostgresDatabase = Depends(get_postgres_client),
) -> PostgresDatabase:
    return ProductRepository(postgres_client)


def get_companies_repository(
    postgres_client: PostgresDatabase = Depends(get_postgres_client),
) -> PostgresDatabase:
    return CompanyRepository(postgres_client)


def get_invoices_repository(
    postgres_client: PostgresDatabase = Depends(get_postgres_client),
) -> PostgresDatabase:
    return InvoiceRepository(postgres_client)


def get_items_repository(
    postgres_client: PostgresDatabase = Depends(get_postgres_client),
) -> PostgresDatabase:
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
