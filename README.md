# NF-e - Nota Fiscal Eletrônica

Python webscrapper for downloading information from a NFe and transform it to JSON.

## Instructions
In order to test this script, run the following command:

```console
> python nfescrapper/main.py --url ~/examples/data.html --out ~/examples/data.json
```

To scrap data from a real URL, let's assume the URL is http://www4.fazenda.rj.gov.br/consultaNFCe/QRCode?p=123, then run the following:

```console
> python nfescrapper/main.py --url "http://www4.fazenda.rj.gov.br/consultaNFCe/QRCode?p=123" --out ~/examples/data.json
```

This will generate a JSON file as such:
```json
{
    "company_name": "ESTABELECIMENTO",
    "cnpj": "12.345.678/0000-00",
    "address": "RUA UM , 000008 , E 000 LJ A , BAIRRO , CIDADE , ES",
    "total_items": 37.0,
    "total_value": 262.52,
    "discounts": 3.98,
    "total_to_pay": 258.54,
    "how_paid": "Dinheiro",
    "total_paied": 258.54,
    "exchange": 0.0,
    "taxes": 59.92,
    "items": [
        {
            "product": "PRODUTO 1",
            "code": "00000001",
            "quantity": 1.0,
            "uom": "UN: UN",
            "unitary_price": 16.99,
            "total": 16.99
        },
    ]
}
```

## Improvements
- [ ] Convert data to CSV format
- [ ] Generalize products' names avoiding duplicates
- [ ] Generalize company name' names avoiding duplicates
- [ ] Get address localtion with geo coordinates
