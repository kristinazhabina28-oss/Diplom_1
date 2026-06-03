import pytest

from praktikum.bun import Bun
from tests.data import BUN_NAME, BUN_NAME_CASES, BUN_PRICE, BUN_PRICE_CASES


class TestBun:
    @pytest.mark.parametrize('name', BUN_NAME_CASES)
    def test_get_name_returns_bun_name(self, name):
        menu_bun = Bun(name, BUN_PRICE)

        assert menu_bun.get_name() == name

    @pytest.mark.parametrize('price', BUN_PRICE_CASES)
    def test_get_price_returns_bun_price(self, price):
        menu_bun = Bun(BUN_NAME, price)

        assert menu_bun.get_price() == price
