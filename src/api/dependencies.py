from functools import lru_cache
from typing import Annotated
from fastapi import Depends
import os
from .database.schema import PostgresDatabase
from .ports.repositories import Repository
from .repositories.product import ProductRepository
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


def get_service_client(
    postgres_client: PostgresDatabase = Depends(get_postgres_client),
) -> PostgresDatabase:
    return ProductRepository(postgres_client)


def get_products_services(
    repository: Annotated[ProductRepository, Depends(get_service_client)],
) -> Service:
    return ProductService(repository)
