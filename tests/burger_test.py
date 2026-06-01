import pytest

from praktikum.ingredient_types import INGREDIENT_TYPE_FILLING, INGREDIENT_TYPE_SAUCE


class TestBurgerInit:
    def test_new_burger_has_no_bun(self, burger):
        assert burger.bun is None

    def test_new_burger_has_empty_ingredients(self, burger):
        assert burger.ingredients == []


class TestSetBuns:
    def test_set_buns_assigns_bun(self, burger, bun_mock):
        burger.set_buns(bun_mock)
        assert burger.bun is bun_mock


class TestAddIngredient:
    @pytest.mark.parametrize('ingredient_type,name', [
        (INGREDIENT_TYPE_SAUCE, 'hot sauce'),
        (INGREDIENT_TYPE_FILLING, 'cutlet'),
    ])
    def test_add_ingredient_appends(self, burger, make_ingredient, ingredient_type, name):
        ingredient = make_ingredient(ingredient_type=ingredient_type, name=name)
        burger.add_ingredient(ingredient)
        assert burger.ingredients == [ingredient]

    def test_add_several_ingredients_keeps_order(self, burger, make_ingredient):
        first = make_ingredient(name='one')
        second = make_ingredient(name='two')
        burger.add_ingredient(first)
        burger.add_ingredient(second)
        assert burger.ingredients == [first, second]


class TestRemoveIngredient:
    def test_remove_ingredient_by_index(self, burger, make_ingredient):
        first = make_ingredient(name='one')
        second = make_ingredient(name='two')
        burger.add_ingredient(first)
        burger.add_ingredient(second)
        burger.remove_ingredient(0)
        assert burger.ingredients == [second]


class TestMoveIngredient:
    def test_move_ingredient_changes_order(self, burger, make_ingredient):
        first = make_ingredient(name='one')
        second = make_ingredient(name='two')
        third = make_ingredient(name='three')
        for ingredient in (first, second, third):
            burger.add_ingredient(ingredient)
        burger.move_ingredient(0, 2)
        assert burger.ingredients == [second, third, first]


class TestGetPrice:
    @pytest.mark.parametrize('bun_price,ingredient_prices,expected', [
        (100, [], 200),
        (100, [50], 250),
        (200, [50, 150], 600),
    ])
    def test_get_price(self, burger, bun_mock, make_ingredient,
                       bun_price, ingredient_prices, expected):
        bun_mock.get_price.return_value = bun_price
        burger.set_buns(bun_mock)
        for price in ingredient_prices:
            burger.add_ingredient(make_ingredient(price=price))

        assert burger.get_price() == expected

    def test_get_price_uses_bun_price(self, burger, bun_mock):
        burger.set_buns(bun_mock)
        burger.get_price()
        bun_mock.get_price.assert_called_once_with()


class TestGetReceipt:
    def test_receipt_without_ingredients(self, burger, bun_mock):
        burger.set_buns(bun_mock)
        expected = (
            '(==== black bun ====)\n'
            '(==== black bun ====)\n\n'
            'Price: 200'
        )
        assert burger.get_receipt() == expected

    def test_receipt_with_ingredients(self, burger, bun_mock, make_ingredient):
        burger.set_buns(bun_mock)
        burger.add_ingredient(make_ingredient(INGREDIENT_TYPE_SAUCE, 'hot sauce', 100))
        burger.add_ingredient(make_ingredient(INGREDIENT_TYPE_FILLING, 'cutlet', 200))
        expected = (
            '(==== black bun ====)\n'
            '= sauce hot sauce =\n'
            '= filling cutlet =\n'
            '(==== black bun ====)\n\n'
            'Price: 500'
        )
        assert burger.get_receipt() == expected
