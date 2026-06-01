from praktikum.bun import Bun
from praktikum.database import Database
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_FILLING, INGREDIENT_TYPE_SAUCE


class TestDatabase:
    def test_available_buns_returns_buns_from_database(self):
        database = Database()

        buns = database.available_buns()

        assert buns is database.buns
        assert all(isinstance(bun, Bun) for bun in buns)
        assert [bun.get_name() for bun in buns] == ['black bun', 'white bun', 'red bun']
        assert [bun.get_price() for bun in buns] == [100, 200, 300]

    def test_available_ingredients_returns_ingredients_from_database(self):
        database = Database()

        ingredients = database.available_ingredients()

        assert ingredients is database.ingredients
        assert all(isinstance(ingredient, Ingredient) for ingredient in ingredients)
        assert [ingredient.get_type() for ingredient in ingredients] == [
            INGREDIENT_TYPE_SAUCE,
            INGREDIENT_TYPE_SAUCE,
            INGREDIENT_TYPE_SAUCE,
            INGREDIENT_TYPE_FILLING,
            INGREDIENT_TYPE_FILLING,
            INGREDIENT_TYPE_FILLING,
        ]
        assert [ingredient.get_name() for ingredient in ingredients] == [
            'hot sauce',
            'sour cream',
            'chili sauce',
            'cutlet',
            'dinosaur',
            'sausage',
        ]
        assert [ingredient.get_price() for ingredient in ingredients] == [100, 200, 300, 100, 200, 300]
