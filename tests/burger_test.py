import pytest

from praktikum.ingredient_types import INGREDIENT_TYPE_FILLING, INGREDIENT_TYPE_SAUCE
from tests.data import (
    BUN_NAME,
    BUN_PRICE,
    FILLING_NAME,
    FILLING_PRICE,
    FINAL_LAYER_NAME,
    FIRST_LAYER_NAME,
    LOWER_LAYER_NAME,
    LOWER_LAYER_PRICE,
    MIDDLE_LAYER_NAME,
    REMAINING_LAYER_NAME,
    REMOVABLE_LAYER_NAME,
    SAUCE_NAME,
    SAUCE_PRICE,
    UPPER_LAYER_NAME,
    UPPER_LAYER_PRICE,
)


class TestFreshBurger:
    def test_receipt_for_new_burger_after_selecting_bun_has_no_ingredients(self, draft_burger, selected_bun):
        draft_burger.set_buns(selected_bun)
        expected = (
            f'(==== {BUN_NAME} ====)\n'
            f'(==== {BUN_NAME} ====)\n\n'
            f'Price: {BUN_PRICE * 2}'
        )

        assert draft_burger.get_receipt() == expected


class TestBurgerAssembly:
    def test_set_buns_uses_selected_bun_in_receipt(self, draft_burger, selected_bun):
        draft_burger.set_buns(selected_bun)

        assert draft_burger.get_receipt().startswith(f'(==== {BUN_NAME} ====)')

    @pytest.mark.parametrize('ingredient_type,name', [
        (INGREDIENT_TYPE_SAUCE, SAUCE_NAME),
        (INGREDIENT_TYPE_FILLING, FILLING_NAME),
    ])
    def test_add_ingredient_adds_layer_to_receipt(self, draft_burger, selected_bun, ingredient_factory,
                                                  ingredient_type, name):
        draft_burger.set_buns(selected_bun)
        order_layer = ingredient_factory(ingredient_type=ingredient_type, name=name)

        draft_burger.add_ingredient(order_layer)

        assert f'= {ingredient_type.lower()} {name} =' in draft_burger.get_receipt()

    def test_added_layers_keep_queue_order(self, draft_burger, selected_bun, ingredient_factory):
        draft_burger.set_buns(selected_bun)
        lower_layer = ingredient_factory(name=LOWER_LAYER_NAME, price=LOWER_LAYER_PRICE)
        upper_layer = ingredient_factory(name=UPPER_LAYER_NAME, price=UPPER_LAYER_PRICE)
        draft_burger.add_ingredient(lower_layer)
        draft_burger.add_ingredient(upper_layer)
        expected = (
            f'(==== {BUN_NAME} ====)\n'
            f'= {INGREDIENT_TYPE_FILLING.lower()} {LOWER_LAYER_NAME} =\n'
            f'= {INGREDIENT_TYPE_FILLING.lower()} {UPPER_LAYER_NAME} =\n'
            f'(==== {BUN_NAME} ====)\n\n'
            f'Price: {BUN_PRICE * 2 + LOWER_LAYER_PRICE + UPPER_LAYER_PRICE}'
        )

        assert draft_burger.get_receipt() == expected

    def test_remove_ingredient_deletes_layer_by_position(self, draft_burger, selected_bun, ingredient_factory):
        draft_burger.set_buns(selected_bun)
        removable_layer = ingredient_factory(name=REMOVABLE_LAYER_NAME)
        remaining_layer = ingredient_factory(name=REMAINING_LAYER_NAME)
        draft_burger.add_ingredient(removable_layer)
        draft_burger.add_ingredient(remaining_layer)

        draft_burger.remove_ingredient(0)

        receipt = draft_burger.get_receipt()
        assert f'= {INGREDIENT_TYPE_FILLING.lower()} {REMOVABLE_LAYER_NAME} =' not in receipt
        assert f'= {INGREDIENT_TYPE_FILLING.lower()} {REMAINING_LAYER_NAME} =' in receipt

    def test_move_ingredient_moves_layer_to_requested_position(self, draft_burger, selected_bun, ingredient_factory):
        draft_burger.set_buns(selected_bun)
        first_layer = ingredient_factory(name=FIRST_LAYER_NAME)
        middle_layer = ingredient_factory(name=MIDDLE_LAYER_NAME)
        final_layer = ingredient_factory(name=FINAL_LAYER_NAME)
        for order_layer in (first_layer, middle_layer, final_layer):
            draft_burger.add_ingredient(order_layer)

        draft_burger.move_ingredient(0, 2)
        receipt_lines = draft_burger.get_receipt().splitlines()

        assert receipt_lines[1:4] == [
            f'= {INGREDIENT_TYPE_FILLING.lower()} {MIDDLE_LAYER_NAME} =',
            f'= {INGREDIENT_TYPE_FILLING.lower()} {FINAL_LAYER_NAME} =',
            f'= {INGREDIENT_TYPE_FILLING.lower()} {FIRST_LAYER_NAME} =',
        ]


class TestGetPrice:
    @pytest.mark.parametrize('bun_price,ingredient_prices,expected', [
        (90, (), 180),
        (120, (35,), 275),
        (145, (15, 40, 60), 405),
    ])
    def test_get_price(self, draft_burger, selected_bun, ingredient_factory,
                       bun_price, ingredient_prices, expected):
        selected_bun.get_price.return_value = bun_price
        draft_burger.set_buns(selected_bun)
        for layer_price in ingredient_prices:
            draft_burger.add_ingredient(ingredient_factory(price=layer_price))

        assert draft_burger.get_price() == expected

    def test_get_price_uses_bun_price(self, draft_burger, selected_bun):
        draft_burger.set_buns(selected_bun)
        draft_burger.get_price()
        selected_bun.get_price.assert_called_once_with()


class TestReceiptText:
    def test_receipt_without_ingredients(self, draft_burger, selected_bun):
        draft_burger.set_buns(selected_bun)
        expected = (
            f'(==== {BUN_NAME} ====)\n'
            f'(==== {BUN_NAME} ====)\n\n'
            f'Price: {BUN_PRICE * 2}'
        )
        assert draft_burger.get_receipt() == expected

    def test_receipt_lists_layers_and_final_price(self, draft_burger, selected_bun, ingredient_factory):
        draft_burger.set_buns(selected_bun)
        draft_burger.add_ingredient(ingredient_factory(INGREDIENT_TYPE_SAUCE, SAUCE_NAME, SAUCE_PRICE))
        draft_burger.add_ingredient(ingredient_factory(INGREDIENT_TYPE_FILLING, FILLING_NAME, FILLING_PRICE))
        expected = (
            f'(==== {BUN_NAME} ====)\n'
            f'= {INGREDIENT_TYPE_SAUCE.lower()} {SAUCE_NAME} =\n'
            f'= {INGREDIENT_TYPE_FILLING.lower()} {FILLING_NAME} =\n'
            f'(==== {BUN_NAME} ====)\n\n'
            f'Price: {BUN_PRICE * 2 + SAUCE_PRICE + FILLING_PRICE}'
        )
        assert draft_burger.get_receipt() == expected
