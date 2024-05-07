from dataclasses import dataclass
from enum import Enum

__all__ = ["Address", "PaymentType", "Taxes", "Totals"]


class PaymentType(Enum):
    CASH = "DINHEIRO"
    CREDIT_CARD = "CARTÃO DE CRÉDITO"
    DEBIT_CARD = "CARTÃO DE DÉBITO"
    PIX = "PIX"

    @staticmethod
    def from_str(label):
        if label in ("DINHEIRO",):
            return PaymentType.CASH
        elif label in ("CARTÃO DE DÉBITO", "CARTÃO DÉBITO", "DÉBITO"):
            return PaymentType.DEBIT_CARD
        elif label in ("CARTÃO DE CRÉDITO", "CRÉDITO"):
            return PaymentType.CREDIT_CARD
        elif label in ("PIX",):
            return PaymentType.PIX
        else:
            raise NotImplementedError


@dataclass
class Address:
    street: str = ""
    number: str = ""
    complement: str = ""
    neighborhood: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""


@dataclass
class Totals:
    payment_type: PaymentType
    discounts: float = 0.0
    exchange: float = 0.0
    total_before_discount: float = 0.0
    total_after_discount: float = 0.0
    total_items: int = 0


@dataclass
class Taxes:
    federal: float = 0.0
    state: float = 0.0
    municipal: float = 0.0
    source: str = ""

    @property
    def total(self) -> float:
        return self.federal + self.state + self.municipal
