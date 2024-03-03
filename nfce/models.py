from datetime import datetime
from dataclasses import dataclass
from typing import List

from enum import StrEnum


class TipoPagamento(StrEnum):
    DINHEIRO = "Dinheiro"
    CARTAO_CREDITO = "Cartão de Crédito"
    CARTAO_DEBITO = "Cartão de Débito"
    PIX = "PIX"


@dataclass
class Empresa:
    razao_social: str
    cnpj: str
    endereco: str


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


@dataclass
class Totais:
    itens: List[Item]
    desconto: float = 0.0
    imposto: float = 0.0
    troco: float = 0.0
    tipo_pagamento: TipoPagamento = TipoPagamento.DINHEIRO

    @property
    def valor(self) -> float:
        return sum(item.valor_total for item in self.itens)

    @property
    def quantidade(self) -> int:
        return len(self.itens)

    @property
    def valor_com_desconto(self) -> float:
        return self.valor - self.desconto


@dataclass
class NotaFiscalEletronica:
    empresa: Empresa
    itens: List[Item]
    totais: Totais
    chave_acesso: str
    numero: str
    serie: str
    data_emissao: datetime

    def to_dict(self) -> dict:
        return {
            "chave_acesso": self.chave_acesso,
            "numero": self.numero,
            "serie": self.serie,
            "data_emissao": (
                ""
                if self.data_emissao == ""
                else datetime.strftime(self.data_emissao, "%Y-%m-%d %H:%M:%S%z")
            ),
            "empresa": vars(self.empresa),
            "itens": [vars(item) for item in self.itens],
            "totais": vars(self.totais),
        }
