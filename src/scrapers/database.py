from typing import Any
from domain import EletronicInvoice, Company, Item, Product, Totals, Taxes, Address
from repositories import InvoiceRepository
from repositories.company import CompanyRepository
from repositories.item import ItemRepository
from repositories.product import ProductRepository


def _dict_to_entity(data: dict[str, Any]) -> EletronicInvoice:
    """Transform a dictionary into an entity."""

    address = Address(
        street=data["endereco"]["logradouro"],
        number=data["endereco"]["numero"],
        complement=data["endereco"]["complemento"],
        neighborhood=data["endereco"]["bairro"],
        city=data["endereco"]["municipio"],
        state=data["endereco"]["uf"],
        zip_code=data["endereco"]["cep"],
    )

    items = [
        Item(
            id=0,
            invoice_id=0,
            product_id=0,
            product=Product(
                id=0,
                code=item["codigo_produto"],
                description=item["descricao_produto"],
            ),
            quantity=item["quantidade"],
            unit_price=item["preco_unitario"],
            unity_of_measurement=item["unidade_medida"],
        )
        for item in data["itens"].values()
    ]

    invoice = EletronicInvoice(
        id=0,
        number=data["informacoes"]["numero"],
        series=data["informacoes"]["serie"],
        issue_date=data["informacoes"]["data_emissao"],
        authorization_date=data["informacoes"]["data_autorizacao"],
        authorization_protocol=data["informacoes"]["protocolo_autorizacao"],
        access_key=data["informacoes"]["chave_acesso"],
        company=Company(
            id=0,
            address=address,
            name=data["empresa"]["razao_social"],
            cnpj=data["empresa"]["cnpj"],
        ),
        totals=Totals(
            payment_type=data["totais"]["tipo_pagamento"],
            discounts=data["totais"]["desconto"],
            exchange=data["totais"]["troco"],
            total_after_discount=data["totais"]["valor_a_pagar"],
        ),
        taxes=Taxes(
            federal=data["tributos"]["federal"],
            state=data["tributos"]["estadual"],
            municipal=data["tributos"]["municipal"],
            source=data["tributos"]["fonte"],
        ),
        items=items,
    )

    return invoice


def save_invoice(
    invoice: dict[str, Any],
    invoice_repository: InvoiceRepository,
    company_repository: CompanyRepository,
    product_repository: ProductRepository,
    item_repository: ItemRepository,
):
    """Save the invoice data into the database."""

    entity = _dict_to_entity(invoice)

    invoices = invoice_repository.find_all(access_key=entity.access_key)

    if len(invoices) == 1:
        entity.id = invoices[0].id
    else:
        _entity = invoice_repository.save(entity)
        entity.id = _entity.id

    companies = company_repository.find_all(cnpj=entity.company.cnpj)

    if len(companies) == 1:
        entity.company.id = companies[0].id
    else:
        entity.company = company_repository.save(entity.company)

    for item in entity.items:
        item.invoice_id = entity.id

        products = product_repository.find_all(
            code=item.product.code, description=item.product.description
        )

        if len(products) == 1:
            item.product_id = products[0].id
        else:
            product = product_repository.save(item.product)
            item.product_id = product.id

        items = item_repository.find_all(
            invoice_id=item.invoice_id, product_id=item.product_id
        )

        if len(items) == 1:
            item.id = items[0].id
        else:
            item = item_repository.save(item)
