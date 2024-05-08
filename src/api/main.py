from fastapi import FastAPI
from api.routers import companies, items, products, invoices

app = FastAPI()

app.include_router(products.router)
app.include_router(companies.router)
app.include_router(invoices.router)
app.include_router(items.router)
