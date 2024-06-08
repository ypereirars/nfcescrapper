from src.domain import Taxes


def test_sum_total_taxes():
    taxes = Taxes(federal=10.0, state=5.0, municipal=2.5)
    assert taxes.total == 17.5
