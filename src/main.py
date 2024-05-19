from fastapi import FastAPI
from routers import companies_router, invoices_router, items_router, products_router

app = FastAPI()

app.include_router(products_router)
app.include_router(companies_router)
app.include_router(invoices_router)
app.include_router(items_router)
