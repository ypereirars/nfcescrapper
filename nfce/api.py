from fastapi import FastAPI
from .services import scrape_invoice
from nfce.database import save

app = FastAPI()


@app.post("/nfce", status_code=201)
def scrape_nfce(url: str = "", chave_acesso: str = ""):
    if not url and not chave_acesso:
        return {"error": "You must provide either a URL or a chave de acesso"}

    if chave_acesso:
        url = f"http://www4.fazenda.rj.gov.br/consultaNFCe/QRCode?chNFe={chave_acesso}&nVersao=200&tpAmb=1&cDest=&dhEmi=323032342d30342d30345431393a32303a34362d30333a3030&vNF=479.90&vICMS=0.00&digVal=476334516767776c6a702b763336476f723649432b656f574552593d&cIdToken=000001&cHashQRCode=3195E103D2F5B324A8C41B6C1E9989142AEE01DD"
    try:
        invoice = scrape_invoice(url)
    except Exception as e:
        print(f"Failed to scrape {e}")
        return {"error": str(e)}

    try:
        print("Saving invoice")
        save(invoice)
        return {"message": "Invoice saved"}
    except Exception as e:
        print(f"Failed to save {e}")
        return {"error": str(e)}
