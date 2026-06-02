import pytest

from praktikum.bun import Bun


class TestBun:
    @pytest.mark.parametrize('name,price', [
        ('sesame bun', 45),
        ('potato bun', 65),
        ('rye bun', 85),
    ])
    def test_bun_has_name_and_price(self, name, price):
        menu_bun = Bun(name, price)

        assert menu_bun.get_name() == name
        assert menu_bun.get_price() == price
