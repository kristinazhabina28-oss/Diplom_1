import pytest

from praktikum.ingredient import Ingredient
from tests.data import (
    INGREDIENT_NAME,
    INGREDIENT_NAME_CASES,
    INGREDIENT_PRICE,
    INGREDIENT_PRICE_CASES,
    INGREDIENT_TYPE,
    INGREDIENT_TYPE_CASES,
)


class TestIngredient:
    @pytest.mark.parametrize('ingredient_type', INGREDIENT_TYPE_CASES)
    def test_get_type_returns_ingredient_type(self, ingredient_type):
        menu_item = Ingredient(ingredient_type, INGREDIENT_NAME, INGREDIENT_PRICE)

        assert menu_item.get_type() == ingredient_type

    @pytest.mark.parametrize('name', INGREDIENT_NAME_CASES)
    def test_get_name_returns_ingredient_name(self, name):
        menu_item = Ingredient(INGREDIENT_TYPE, name, INGREDIENT_PRICE)

        assert menu_item.get_name() == name

    @pytest.mark.parametrize('price', INGREDIENT_PRICE_CASES)
    def test_get_price_returns_ingredient_price(self, price):
        menu_item = Ingredient(INGREDIENT_TYPE, INGREDIENT_NAME, price)

        assert menu_item.get_price() == price
