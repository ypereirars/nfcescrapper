from fastapi import FastAPI
from api.routers import products

app = FastAPI()

app.include_router(products.router)
