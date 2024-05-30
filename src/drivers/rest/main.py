from fastapi import FastAPI

from drivers.rest.exceptions_handler import exception_container
from .routers import (
    companies_router,
    invoices_router,
    items_router,
    products_router,
    users_router,
)

app = FastAPI()

app.include_router(products_router)
app.include_router(companies_router)
app.include_router(invoices_router)
app.include_router(items_router)
app.include_router(users_router)

exception_container(app)
