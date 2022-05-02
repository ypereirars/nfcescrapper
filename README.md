# NFC-e - Nota Fiscal de Consumidor Eletrônica

Python webscrapper for downloading information from a NFe and serialize it to JSON or CSV (other formats may be supported in future version).

## Setup
Create a virtual environment:

```shell
$ python -m venv .venv/nfce
$ source .venv/nfce/bin/activate
```

and then upgrade pip and install dependencies:

```shell
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt
```

Or install the application:
```shell
$ pip install .
```
*⚠️Note: you may have to install: *
```shell
$ pip install wheel
```

## Instructions

### Install Chrome & chromedriver
If you already have Chrome installed, you can skip this part. First, you need to download and install the Google Chrome:

```shell
$ sudo apt update
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo dpkg -i google-chrome-stable_current_amd64.deb
$ sudo apt-get install -f
$ google-chrome --version
```

Then, download and install `chromedriver`:

```shell
$ wget https://chromedriver.storage.googleapis.com/<version>/chromedriver_linux64.zip
$ unzip chromedriver_linux64.zip
$ sudo mv chromedriver /usr/bin/chromedriver
$ sudo chown root:root /usr/bin/chromedriver
$ sudo chmod +x /usr/bin/chromedriver
```

From now, you might have chromedriver!

### Run the application
In order to test this script, run the following command:

```console
> python nfescrapper/main.py\
--url ~/examples/data.html\
--out ~/examples/data.json
```

*chromedriver path may also be provided via `--webdriver-path path/to/chromedriver`*

To scrap data from a real URL, let's assume the URL is http://www4.fazenda.rj.gov.br/consultaNFCe/QRCode?p=123, then run the following:

```console
> python nfescrapper/main.py\
--url "http://www4.fazenda.rj.gov.br/consultaNFCe/QRCode?p=123"\
--out ~/examples/data.json
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
    "tax": 59.92,
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

If a `--format csv` flag is provided, then the result will be:

```csv
"name";"cnpj";"address";"exchange";"tax";"payment_type";"total_paid";"total_to_pay";"total_price";"total_items";"discounts";"code";"name";"quantity";"unity_of_measure";"price";"currency";"total_price"
"ESTABELECIMENTO";"12.345.678/0000-00";"RUA UM,000008,E 000 LJ A,BAIRRO,CIDADE,ES";0.0;59.92;"Dinheiro";258.54;258.54;262.52;37.0;3.98;"00000001";"PRODUTO 1";1.0;"UN";16.99;"R$";16.99
"ESTABELECIMENTO";"12.345.678/0000-00";"RUA UM,000008,E 000 LJ A,BAIRRO,CIDADE,ES";0.0;59.92;"Dinheiro";258.54;258.54;262.52;37.0;3.98;"00000002";"PRODUTO 2";1.0;"UN";2.49;"R$";2.49
"ESTABELECIMENTO";"12.345.678/0000-00";"RUA UM,000008,E 000 LJ A,BAIRRO,CIDADE,ES";0.0;59.92;"Dinheiro";258.54;258.54;262.52;37.0;3.98;"00000003";"PRODUTO 3";1.0;"UN";2.39;"R$";2.39
"ESTABELECIMENTO";"12.345.678/0000-00";"RUA UM,000008,E 000 LJ A,BAIRRO,CIDADE,ES";0.0;59.92;"Dinheiro";258.54;258.54;262.52;37.0;3.98;"00000004";"PRODUTO 4";3.0;"UN";1.69;"R$";5.07
```` 

## Improvements
- [x] Convert data to CSV format
- [ ] Generalize products' names avoiding duplicates
- [ ] Generalize company name' names avoiding duplicates
- [ ] Get address localtion with geo coordinates
