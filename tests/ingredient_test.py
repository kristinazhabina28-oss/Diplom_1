import pytest

from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_FILLING, INGREDIENT_TYPE_SAUCE


class TestIngredient:
    @pytest.mark.parametrize('ingredient_type,name,price', [
        (INGREDIENT_TYPE_SAUCE, 'berry sauce', 55),
        (INGREDIENT_TYPE_FILLING, 'cheese cube', 95),
    ])
    def test_ingredient_has_type_name_and_price(self, ingredient_type, name, price):
        menu_item = Ingredient(ingredient_type, name, price)

        assert menu_item.get_type() == ingredient_type
        assert menu_item.get_name() == name
        assert menu_item.get_price() == price
