from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

Base = declarative_base()


class Product(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Text, name="codigo")
    description = Column(Text, name="descricao")


class Company(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(Text, name="cnpj")
    name = Column(Text, name="razao_social")
    street = Column(Text, name="logradouro")
    number = Column(Text, name="numero")
    neighborhood = Column(Text, name="bairro")
    city = Column(Text, name="municipio")
    state = Column(Text, name="uf")
    complement = Column(Text, name="complemento")
    zip_code = Column(Text, name="cep")


class Invoice(Base):
    __tablename__ = "notas_fiscais"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("empresas.id"), name="id_empresa")
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
    company = relationship("Company", backref="notas_fiscais", lazy=True)
    items = relationship("Item", backref="notas_fiscais", lazy=True)


class Item(Base):
    __tablename__ = "itens_nota"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("produtos.id"), name="id_produto")
    invoice_id = Column(Integer, ForeignKey("notas_fiscais.id"), name="id_nota_fiscal")
    quantity = Column(Integer, name="quantidade")
    price = Column(Integer, name="preco_unitario")
    unit_of_measurement = Column(Text, name="unidade_medida")
    product = relationship("Product", backref="notas_fiscais", lazy=True)
    invoice = relationship("Invoice", backref="notas_fiscais", viewonly=True, lazy=True)


class PostgresDatabase:
    def __init__(
        self,
        database: str,
        username: str,
        password: str,
        host: str = "0.0.0.0",
        port: int = 5432,
    ):
        engine = create_engine(
            f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
        )

        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)
        self.Product = Product
        self.Company = Company
        self.Invoice = Invoice
        self.Item = Item

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def __enter__(self) -> Session:
        return self.Session()

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.Session().close()
