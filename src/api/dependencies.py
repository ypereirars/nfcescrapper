from functools import lru_cache
from typing import Annotated
from fastapi import Depends
import os

from api.repositories.company import CompanyRepository
from .database.schema import PostgresDatabase
from .ports.repositories import Repository
from .repositories.product import ProductRepository
from .services.services import CompanyService
from .services.services import ProductService
from .ports.services import Service

from dotenv import load_dotenv

load_dotenv()


@lru_cache
def get_postgres_client() -> PostgresDatabase:
    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")

    if all([database, user, password, host]):
        return PostgresDatabase(database, user, password, host=host)

    raise ValueError("Missing environment variables for Postgres connection")


def get_products_repository(
    postgres_client: PostgresDatabase = Depends(get_postgres_client),
) -> PostgresDatabase:
    return ProductRepository(postgres_client)


def get_companies_repository(
    postgres_client: PostgresDatabase = Depends(get_postgres_client),
) -> PostgresDatabase:
    return CompanyRepository(postgres_client)


def get_products_services(
    repository: Annotated[ProductRepository, Depends(get_products_repository)],
) -> Service:
    return ProductService(repository)


def get_companies_services(
    repository: Annotated[CompanyRepository, Depends(get_companies_repository)],
) -> Service:
    return CompanyService(repository)
