from repositories import UserRepository
from repositories.company import CompanyRepository
from repositories.invoice import InvoiceRepository
from repositories.item import ItemRepository
from repositories.product import ProductRepository
from services.company import CompanyService
from services.invoice import InvoiceService
from services.item import ItemService
from services.product import ProductService
from services.user import UserService
from settings.database import get_db_connection
from functools import lru_cache

__all__ = [
    "get_user_service",
    "get_company_service",
    "get_product_service",
    "get_invoice_service",
    "get_items_services",
]


@lru_cache
def get_user_service() -> UserService:
    database = next(get_db_connection())

    return UserService(UserRepository(database))


@lru_cache
def get_company_service() -> CompanyService:
    database = next(get_db_connection())

    return CompanyService(CompanyRepository(database))


@lru_cache
def get_product_service() -> ProductService:
    database = next(get_db_connection())

    return ProductService(ProductRepository(database))


@lru_cache
def get_invoice_service() -> InvoiceService:
    database = next(get_db_connection())

    return InvoiceService(InvoiceRepository(database))


@lru_cache
def get_items_services() -> ItemService:
    database = next(get_db_connection())

    return ItemService(ItemRepository(database))
