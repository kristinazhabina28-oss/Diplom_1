from unittest.mock import Mock

import pytest

from praktikum.bun import Bun
from praktikum.burger import Burger
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_FILLING


@pytest.fixture
def draft_burger():
    return Burger()


@pytest.fixture
def selected_bun():
    bun_double = Mock(spec=Bun)
    bun_double.get_name.return_value = 'nebula bun'
    bun_double.get_price.return_value = 125
    return bun_double


@pytest.fixture
def ingredient_factory():
    def _create(ingredient_type=INGREDIENT_TYPE_FILLING, name='crater cheese', price=75):
        ingredient_double = Mock(spec=Ingredient)
        ingredient_double.get_type.return_value = ingredient_type
        ingredient_double.get_name.return_value = name
        ingredient_double.get_price.return_value = price
        return ingredient_double

    return _create
