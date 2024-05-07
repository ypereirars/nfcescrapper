from functools import lru_cache
from typing import Annotated
from fastapi import Depends
import os
from .database.schema import PostgresDatabase
from .ports.repositories import Repository
from .repositories.repositories import ProductRepository

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
    postgres_client: Annotated[PostgresDatabase, Depends(get_postgres_client)],  # type: ignore
) -> Repository:
    return ProductRepository(postgres_client)
