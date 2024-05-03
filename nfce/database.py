import psycopg2
import os
from .models import Item, Empresa, Produto, NotaFiscalEletronica
import logging

import sys

logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"'
)

console_output_handler = logging.StreamHandler(sys.stderr)
console_output_handler.setFormatter(formatter)
logger.addHandler(console_output_handler)

logger.setLevel(logging.INFO)


def save(invoice: NotaFiscalEletronica):
    connection = psycopg2.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
    )

    try:
        logger.info("Checking if invoice already saved")
        invoice_id = get_invoice_by_key(invoice.informacoes.chave_acesso, connection)

        if invoice_id != 0:
            logger.info(f"Invoice with ID {invoice_id} already saved")
            return

        company_id = get_company_by_cnpj(invoice.empresa.cnpj, connection)
        if company_id == 0:
            logger.info("Saving company")
            company_id = save_company(invoice.empresa, connection)

        logger.info(f"Company ID: {company_id}")

        logger.info("Saving invoice")
        invoice_id = save_invoice(invoice, company_id, connection)
        logger.info("Invoice ID", invoice_id)

        logger.info("Saving products")
        product_ids = save_product((item.produto for item in invoice.itens), connection)

        logger.info("Saving invoice items")
        items_id = save_invoice_items(
            invoice_id, product_ids, invoice.itens, connection
        )

        if (
            company_id > 0
            and invoice_id > 0
            and len(product_ids) > 0
            and len(items_id) > 0
        ):
            connection.commit()
            logger.info("Invoice saved")
        else:
            logger.error("Error saving invoice")
            connection.rollback()
    except Exception as ex:
        logger.error("Error saving", ex)
        connection.rollback()
    finally:
        connection.close()

    return invoice_id


def save_company(company: Empresa, connection):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """INSERT INTO empresas
                    (cnpj, razao_social, logradouro, numero, complemento, bairro, municipio, uf, cep)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;""",
                (
                    company.cnpj,
                    company.razao_social,
                    company.endereco.logradouro,
                    company.endereco.numero,
                    company.endereco.complemento,
                    company.endereco.bairro,
                    company.endereco.municipio,
                    company.endereco.uf,
                    company.endereco.cep,
                ),
            )
            id = cursor.fetchone()
            if id:
                return id[0]
        except Exception as ex:
            print("Error saving company", ex)

    return 0


def get_company_by_cnpj(cnpj: str, connection):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """SELECT id FROM empresas WHERE cnpj = %s;""",
                (cnpj,),
            )
            id = cursor.fetchone()
            if id:
                return id[0]
        except Exception as ex:
            print("Error getting company", ex)
    return 0


def get_invoice_by_key(key: str, connection):
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                """SELECT id FROM notas_fiscais WHERE chave_acesso = %s;""",
                (key,),
            )
            id = cursor.fetchone()
            if id:
                return id[0]
        except Exception as ex:
            print("Error getting invoice", ex)
    return 0


def save_invoice(invoice: NotaFiscalEletronica, company_id, connection):
    query = """INSERT INTO notas_fiscais
    (
        id_empresa,
        chave_acesso,
        numero,
        serie,
        protocolo_autorizacao,
        data_autorizacao,
        data_emissao,
        tributacao_federal,
        tributacao_estadual,
        tributacao_municipal,
        fonte
    )
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""

    with connection.cursor() as cursor:
        try:
            cursor.execute(
                query,
                (
                    company_id,
                    invoice.informacoes.chave_acesso,
                    invoice.informacoes.numero,
                    invoice.informacoes.serie,
                    invoice.informacoes.protocolo_autorizacao,
                    invoice.informacoes.data_autorizacao,
                    invoice.informacoes.data_emissao,
                    invoice.informacoes.tributacao.federal,
                    invoice.informacoes.tributacao.estadual,
                    invoice.informacoes.tributacao.municipal,
                    invoice.informacoes.tributacao.fonte,
                ),
            )
            id = cursor.fetchone()
            if id:
                return id[0]
        except Exception:
            print("Error saving invoice")
    return 0


def save_product(products: list[Produto], connection):
    with connection.cursor() as cursor:
        try:
            values = ",".join(
                cursor.mogrify("(%s,%s)", (product.codigo, product.descricao)).decode(
                    "utf-8"
                )
                for product in products
            )

            cursor.execute(
                f"""INSERT INTO produtos (codigo, descricao) VALUES {values} RETURNING id;"""
            )
            ids = cursor.fetchall()
            if ids:
                return [id[0] for id in ids]
        except Exception as ex:
            print("Error saving products", ex)
        return []


def save_invoice_items(
    invoice_id: int, product_ids: list[int], items: list[Item], connection
):
    with connection.cursor() as cursor:
        try:
            values = ",".join(
                cursor.mogrify(
                    "(%s,%s,%s,%s,%s)",
                    (
                        invoice_id,
                        product_id,
                        item.quantidade,
                        item.preco_unitario,
                        item.unidade_medida,
                    ),
                ).decode("utf-8")
                for product_id, item in zip(product_ids, items)
            )

            cursor.execute(
                f"""INSERT INTO itens_nota
                    (id_nota_fiscal, id_produto, quantidade, preco_unitario, unidade_medida)
                    VALUES {values} RETURNING id;""",
            )
            ids = cursor.fetchall()
            if ids:
                return [id[0] for id in ids]
        except Exception:
            print("Error saving items")
        return []
