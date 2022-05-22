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
*⚠️Note: you may have to install:*
```shell
$ pip install wheel
```

## Instructions

### Run the application
There's no need to install webdriver. `ChromeDriverManager` will download and install the lastest chrome driver.

#### Available arguments:
```
usage: python -m main <url to nfe> -o ~/data.json

Argument                 |Optional|Description
---                      |---     |---
`url`                    | No     | URL to download the NFe.
`--help`, `-h`           | Yes    | Show help message and exit.
`--format`, `-f`         | Yes    | Output file format wich may either be json or csv.
`--output`, `-o`         | Yes    | File path location where to save data.
```

*For more information, `python -m main -h`*

To scrap data run the following command, wich will export the result to `~/data.json`:

```console
> python nfescrapper/main.py <url to nfe> -o ~/data.json
```

#### Example
Below is an example of a JSON file:
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
