from fastapi import FastAPI
from .services import scrape_invoice

app = FastAPI()


@app.get("/nfce")
def scrape_nfce(url: str):
    invoice = scrape_invoice(url)
    return vars(invoice)
