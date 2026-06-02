from praktikum.bun import Bun
from praktikum.database import Database
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_FILLING, INGREDIENT_TYPE_SAUCE


EXPECTED_BUNS = (
    ('black bun', 100),
    ('white bun', 200),
    ('red bun', 300),
)

EXPECTED_INGREDIENTS = (
    (INGREDIENT_TYPE_SAUCE, 'hot sauce', 100),
    (INGREDIENT_TYPE_SAUCE, 'sour cream', 200),
    (INGREDIENT_TYPE_SAUCE, 'chili sauce', 300),
    (INGREDIENT_TYPE_FILLING, 'cutlet', 100),
    (INGREDIENT_TYPE_FILLING, 'dinosaur', 200),
    (INGREDIENT_TYPE_FILLING, 'sausage', 300),
)


class TestDatabase:
    def test_available_buns_match_seeded_menu(self):
        storage = Database()

        stored_buns = storage.available_buns()
        actual_buns = tuple((bun.get_name(), bun.get_price()) for bun in stored_buns)

        assert stored_buns is storage.buns
        assert all(isinstance(bun, Bun) for bun in stored_buns)
        assert actual_buns == EXPECTED_BUNS

    def test_available_ingredients_match_seeded_menu(self):
        storage = Database()

        stored_ingredients = storage.available_ingredients()
        actual_ingredients = tuple(
            (ingredient.get_type(), ingredient.get_name(), ingredient.get_price())
            for ingredient in stored_ingredients
        )

        assert stored_ingredients is storage.ingredients
        assert all(isinstance(ingredient, Ingredient) for ingredient in stored_ingredients)
        assert actual_ingredients == EXPECTED_INGREDIENTS
