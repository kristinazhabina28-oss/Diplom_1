from praktikum.ingredient_types import INGREDIENT_TYPE_FILLING, INGREDIENT_TYPE_SAUCE


class TestIngredientTypes:
    def test_ingredient_type_constants(self):
        assert INGREDIENT_TYPE_SAUCE == 'SAUCE'
        assert INGREDIENT_TYPE_FILLING == 'FILLING'
