from typing import Any
from drivers.bots.telegram.dependencies import (
    get_company_repository,
    get_product_repository,
    get_user_repository,
    get_invoice_repository,
    get_items_repository,
)
from drivers.bots.telegram.models import TeleBotUser
from scrapers.scrapers import NfceScraper
from scrapers.utils import is_valid_url, is_valid_access_key
from domain.entities.entities import Company, EletronicInvoice, Item, Product, User
from domain.value_objects.value_objects import Address, Taxes, Totals


URL = "http://www4.fazenda.rj.gov.br/consultaNFCe/QRCode?chNFe={access_key}"


def save_user(user: TeleBotUser) -> TeleBotUser:
    repository = get_user_repository()
    entity = User(
        username=user.username, first_name=user.first_name, last_name=user.last_name
    )

    if repository.find_by_username(user.username) is not None:
        return get_user(user.username)
    model = repository.save(entity)

    return TeleBotUser(
        id=model.id,
        username=model.username,
        first_name=model.first_name,
        last_name=model.last_name,
    )


def get_user(username: str) -> TeleBotUser:
    repository = get_user_repository()

    entity = repository.find_by_username(username)

    if entity is None:
        return None
    else:
        return TeleBotUser(
            id=entity.id,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
        )


def scrape_invoice(input_data: str):
    if is_valid_access_key(input_data):
        url = URL.format(access_key=input_data)
    elif is_valid_url(input_data):
        url = input_data
    else:
        raise ValueError("Invalid input. Please choose between URL or ACCESS KEY.")

    try:
        invoice = NfceScraper().get(url)
        return {"invoice": invoice}
    except Exception as ex:
        return {"invoice": {}, "error": f"Failed to scrape the invoice: {ex}"}


def save_invoice(user: TeleBotUser, invoice_dict: dict[str, Any]):
    user_model = get_user(user.username) or save_user(user)
    company = _get_or_save_company(invoice_dict["empresa"], invoice_dict["endereco"])
    invoice = _get_or_save_invoice(
        invoice_dict["informacoes"], invoice_dict["tributos"], invoice_dict["totais"], company.id, user_model.id
    )

    _save_items(invoice.id, invoice_dict["itens"].values())


def _get_or_save_company(company: dict[str, str], address: dict[str, str]) -> Company:
    repository = get_company_repository()

    address = Address(
        street=address["logradouro"],
        number=address["numero"],
        complement=address["complemento"],
        neighborhood=address["bairro"],
        city=address["municipio"],
        state=address["uf"],
        zip_code=address["cep"],
    )

    entity = Company(
        name=company["razao_social"], cnpj=company["cnpj"], address=address
    )

    model = repository.find_by_cnpj(company["cnpj"])
    
    if model is None:
        model = repository.save(entity)

    return model


def _get_or_save_invoice(
    infos: dict[str, Any], taxes: dict[str, Any], totals: dict[str, Any], company_id, user_id
) -> EletronicInvoice:
    repository = get_invoice_repository()

    taxes_entity = Taxes(
        federal=taxes["federal"],
        state=taxes["estadual"],
        municipal=taxes["municipal"],
        source=taxes["fonte"],
    )

    totals = Totals(
        payment_type=totals["tipo_pagamento"],
        discounts=totals["desconto"],
        exchange=totals["troco"],
        total_before_discount=totals["valor_a_pagar"]+totals["desconto"],
        total_after_discount=totals["valor_a_pagar"],
        total_items=totals["quantidade_itens"],
    )

    entity = EletronicInvoice(
        user_id=user_id,
        company_id=company_id,
        access_key=infos["chave_acesso"],
        number=infos["numero"],
        series=infos["serie"],
        issue_date=infos["data_emissao"],
        authorization_protocol=infos["protocolo_autorizacao"],
        authorization_date=infos["data_autorizacao"],
        taxes=taxes_entity,
        totals=totals
    )

    invoices = repository.find_all(
        access_key=entity.access_key, number=entity.number, series=entity.series
    )

    if invoices is not None and len(invoices) > 0:
        return invoices[0]

    invoice = repository.save(entity)

    return invoice


def _save_items(invoice_id: int, invoice_items: list[dict[str, Any]]):
    product_repository = get_product_repository()
    item_repository = get_items_repository()

    for item in invoice_items:
        products = product_repository.find_all(
            code=item["codigo_produto"], description=item["descricao_produto"]
        )

        if len(products) == 1:
            product_id = products[0].id
        else:
            product = Product(
                code=item["codigo_produto"], description=item["descricao_produto"]
            )
            product = product_repository.save(product)
            product_id = product.id

        items = item_repository.find_all(invoice_id=invoice_id, product_id=product_id)

        if len(items) == 0:
            item = Item(
                invoice_id=invoice_id,
                product_id=product_id,
                quantity=item["quantidade"],
                unit_price=item["preco_unitario"],
                unity_of_measurement=item["unidade_medida"],
            )
            item_repository.save(item)
