from datetime import datetime
from dataclasses import dataclass
from enum import StrEnum


__all__ = [
    "TipoPagamento",
    "Empresa",
    "Produto",
    "Item",
    "Totais",
    "Tributacao",
    "InformacoesNota",
    "NotaFiscalEletronica",
]


class TipoPagamento(StrEnum):
    DINHEIRO = "DINHEIRO"
    CARTAO_CREDITO = "CARTÃO DE CRÉDITO"
    CARTAO_DEBITO = "CARTÃO DE DÉBITO"
    PIX = "PIX"

    @staticmethod
    def from_str(label):
        if label in ("DINHEIRO",):
            return TipoPagamento.DINHEIRO
        elif label in ("CARTÃO DE DÉBITO", "CARTÃO DÉBITO", "DÉBITO"):
            return TipoPagamento.CARTAO_DEBITO
        elif label in ("CARTÃO DE CRÉDITO", "CARTÃO CRÉDITO", "CRÉDITO"):
            return TipoPagamento.CARTAO_CREDITO
        elif label in ("PIX",):
            return TipoPagamento.PIX
        else:
            raise NotImplementedError


@dataclass
class Endereco:
    logradouro: str = ""
    numero: str = ""
    complemento: str = ""
    bairro: str = ""
    municipio: str = ""
    uf: str = ""
    cep: str = ""


@dataclass
class Empresa:
    razao_social: str
    cnpj: str
    endereco: Endereco

    @property
    def __dict__(self):
        return {
            "razao_social": self.razao_social,
            "cnpj": self.cnpj,
            **vars(self.endereco),
        }


@dataclass
class Produto:
    codigo: str
    descricao: str


@dataclass
class Item:
    produto: Produto
    quantidade: int = 1
    preco_unitario: float = 0.0
    unidade_medida: str = "UN"

    @property
    def preco_total(self) -> float:
        return self.preco_unitario * self.quantidade

    @property
    def __dict__(self):
        return {
            **vars(self.produto),
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "unidade_medida": self.unidade_medida,
            "preco_total": self.preco_total,
        }


@dataclass
class Totais:
    desconto: float = 0.0
    troco: float = 0.0
    valor_total: float = 0.0
    valor_a_pagar: float = 0.0
    quantidade_itens: int = 0
    tipo_pagamento: TipoPagamento = TipoPagamento.DINHEIRO


@dataclass
class Tributacao:
    federal: float = 0.0
    estadual: float = 0.0
    municipal: float = 0.0
    fonte: str = ""

    @property
    def total(self) -> float:
        return self.federal + self.estadual + self.municipal


@dataclass
class InformacoesNota:
    chave_acesso: str
    numero: str
    serie: str
    data_emissao: datetime = None
    protocolo_autorizacao: str = ""
    data_autorizacao: datetime = None
    tributacao: Tributacao = None

    @property
    def __dict__(self):
        return {
            "chave_acesso": self.chave_acesso,
            "numero": self.numero,
            "serie": self.serie,
            "data_emissao": (
                self.data_emissao.strftime("%Y-%m-%d %H:%M:%S%z")
                if self.data_emissao
                else ""
            ),
            "protocolo_autorizacao": self.protocolo_autorizacao,
            "data_autorizacao": (
                self.data_autorizacao.strftime("%Y-%m-%d %H:%M:%S%z")
                if self.data_autorizacao
                else ""
            ),
            "tributacao": vars(self.tributacao),
        }


@dataclass
class NotaFiscalEletronica:
    empresa: Empresa
    informacoes: InformacoesNota
    itens: list[Item]
    totais: Totais

    @property
    def __dict__(self):
        return {
            **vars(self.informacoes),
            **vars(self.empresa),
            "itens": {
                **vars(self.totais),
                "produtos": [vars(item) for item in self.itens],
            },
        }
