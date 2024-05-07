from fastapi import FastAPI
from api.routers import companies, products, invoices

app = FastAPI()

app.include_router(products.router)
app.include_router(companies.router)
app.include_router(invoices.router)
