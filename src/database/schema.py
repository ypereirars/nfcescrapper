from datetime import datetime, UTC

from sqlalchemy import Column, DateTime, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base


__all__ = [
    "Schema",
    "UserSchema",
    "ProductSchema",
    "CompanySchema",
    "InvoiceSchema",
    "ItemSchema",
]

Schema = declarative_base()


class UserSchema(Schema):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(Text, name="primeiro_nome")
    last_name = Column(Text, name="ultimo_nome")
    username = Column(Text, name="nome_usuario", unique=True)
    created_on = Column(DateTime, name="data_criacao", default=datetime.now(UTC))


class ProductSchema(Schema):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, name="codigo")
    description = Column(Text, name="descricao")
    created_on = Column(DateTime, name="data_criacao", default=datetime.now(UTC))


class CompanySchema(Schema):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String, name="cnpj")
    name = Column(Text, name="razao_social")
    street = Column(Text, name="logradouro")
    number = Column(String, name="numero")
    neighborhood = Column(Text, name="bairro")
    city = Column(Text, name="municipio")
    state = Column(String, name="uf")
    complement = Column(Text, name="complemento")
    zip_code = Column(String, name="cep")
    created_on = Column(DateTime, name="data_criacao", default=datetime.now(UTC))


class InvoiceSchema(Schema):
    __tablename__ = "notas_fiscais"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("empresas.id"), name="id_empresa")
    user_id = Column(Integer, ForeignKey("usuarios.id"), name="id_usuario")
    access_key = Column(Text, name="chave_acesso")
    number = Column(Text, name="numero")
    series = Column(Text, name="serie")
    issue_date = Column(DateTime, name="data_emissao")
    authorization_protocol = Column(Text, name="protocolo_autorizacao")
    authorization_date = Column(DateTime, name="data_autorizacao")
    federal_tax = Column(Float, name="tributacao_federal")
    state_tax = Column(Float, name="tributacao_estadual")
    city_tax = Column(Float, name="tributacao_municipal")
    source = Column(Text, name="fonte")
    created_on = Column(DateTime, name="data_criacao", default=datetime.now(UTC))
    company = relationship("CompanySchema", backref="notas_fiscais", lazy=True)
    items = relationship("ItemSchema", backref="notas_fiscais", lazy=True)
    user = relationship("UserSchema", backref="notas_fiscais", lazy=True)


class ItemSchema(Schema):
    __tablename__ = "itens_nota"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("produtos.id"), name="id_produto")
    invoice_id = Column(Integer, ForeignKey("notas_fiscais.id"), name="id_nota_fiscal")
    quantity = Column(Float, name="quantidade")
    unit_price = Column(Float, name="preco_unitario")
    unity_of_measurement = Column(Text, name="unidade_medida")
    created_on = Column(DateTime, name="data_criacao", default=datetime.now(UTC))
    product = relationship("ProductSchema", backref="notas_fiscais", lazy=True)
    invoice = relationship(
        "InvoiceSchema", backref="notas_fiscais", viewonly=True, lazy=True
    )
