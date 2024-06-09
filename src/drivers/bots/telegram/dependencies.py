from repositories import UserRepository
from repositories.company import CompanyRepository
from repositories.invoice import InvoiceRepository
from repositories.item import ItemRepository
from repositories.product import ProductRepository
from settings.database import get_db_connection
from functools import lru_cache

__all__ = [
    "get_user_repository",
    "get_company_repository",
    "get_product_repository",
    "get_invoice_repository",
    "get_items_repository",
]


@lru_cache
def get_user_repository() -> UserRepository:
    database = next(get_db_connection())

    return UserRepository(database)


@lru_cache
def get_company_repository() -> CompanyRepository:
    database = next(get_db_connection())

    return CompanyRepository(database)


@lru_cache
def get_product_repository() -> ProductRepository:
    database = next(get_db_connection())

    return ProductRepository(database)


@lru_cache
def get_invoice_repository() -> InvoiceRepository:
    database = next(get_db_connection())

    return InvoiceRepository(database)


@lru_cache
def get_items_repository() -> ItemRepository:
    database = next(get_db_connection())

    return ItemRepository(database)
