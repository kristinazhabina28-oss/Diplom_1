from unittest.mock import Mock

import pytest

from praktikum.bun import Bun
from praktikum.burger import Burger
from praktikum.ingredient import Ingredient
from tests.data import BUN_NAME, BUN_PRICE, INGREDIENT_NAME, INGREDIENT_PRICE, INGREDIENT_TYPE


@pytest.fixture
def draft_burger():
    return Burger()


@pytest.fixture
def selected_bun():
    bun_double = Mock(spec=Bun)
    bun_double.get_name.return_value = BUN_NAME
    bun_double.get_price.return_value = BUN_PRICE
    return bun_double


@pytest.fixture
def ingredient_factory():
    def _create(ingredient_type=INGREDIENT_TYPE, name=INGREDIENT_NAME, price=INGREDIENT_PRICE):
        ingredient_double = Mock(spec=Ingredient)
        ingredient_double.get_type.return_value = ingredient_type
        ingredient_double.get_name.return_value = name
        ingredient_double.get_price.return_value = price
        return ingredient_double

    return _create
