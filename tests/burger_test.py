import pytest

from praktikum.ingredient_types import INGREDIENT_TYPE_FILLING, INGREDIENT_TYPE_SAUCE


class TestFreshBurger:
    def test_new_burger_has_no_bun(self, draft_burger):
        assert draft_burger.bun is None

    def test_new_burger_has_empty_ingredients(self, draft_burger):
        assert draft_burger.ingredients == []


class TestBurgerAssembly:
    def test_selected_bun_is_saved(self, draft_burger, selected_bun):
        draft_burger.set_buns(selected_bun)
        assert draft_burger.bun is selected_bun

    @pytest.mark.parametrize('ingredient_type,name', [
        (INGREDIENT_TYPE_SAUCE, 'galaxy glaze'),
        (INGREDIENT_TYPE_FILLING, 'meteor patty'),
    ])
    def test_new_layer_goes_to_the_end(self, draft_burger, ingredient_factory, ingredient_type, name):
        order_layer = ingredient_factory(ingredient_type=ingredient_type, name=name)
        draft_burger.add_ingredient(order_layer)
        assert draft_burger.ingredients == [order_layer]

    def test_added_layers_keep_queue_order(self, draft_burger, ingredient_factory):
        lower_layer = ingredient_factory(name='orbit onion')
        upper_layer = ingredient_factory(name='plasma tomato')
        draft_burger.add_ingredient(lower_layer)
        draft_burger.add_ingredient(upper_layer)
        assert draft_burger.ingredients == [lower_layer, upper_layer]

    def test_layer_can_be_deleted_by_position(self, draft_burger, ingredient_factory):
        removable_layer = ingredient_factory(name='old layer')
        remaining_layer = ingredient_factory(name='keeper layer')
        draft_burger.add_ingredient(removable_layer)
        draft_burger.add_ingredient(remaining_layer)
        draft_burger.remove_ingredient(0)
        assert draft_burger.ingredients == [remaining_layer]

    def test_layer_moves_to_requested_position(self, draft_burger, ingredient_factory):
        first_layer = ingredient_factory(name='first')
        middle_layer = ingredient_factory(name='middle')
        final_layer = ingredient_factory(name='final')
        for order_layer in (first_layer, middle_layer, final_layer):
            draft_burger.add_ingredient(order_layer)
        draft_burger.move_ingredient(0, 2)
        assert draft_burger.ingredients == [middle_layer, final_layer, first_layer]


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
            '(==== nebula bun ====)\n'
            '(==== nebula bun ====)\n\n'
            'Price: 250'
        )
        assert draft_burger.get_receipt() == expected

    def test_receipt_lists_layers_and_final_price(self, draft_burger, selected_bun, ingredient_factory):
        draft_burger.set_buns(selected_bun)
        draft_burger.add_ingredient(ingredient_factory(INGREDIENT_TYPE_SAUCE, 'green sauce', 30))
        draft_burger.add_ingredient(ingredient_factory(INGREDIENT_TYPE_FILLING, 'moon cutlet', 80))
        expected = (
            '(==== nebula bun ====)\n'
            '= sauce green sauce =\n'
            '= filling moon cutlet =\n'
            '(==== nebula bun ====)\n\n'
            'Price: 360'
        )
        assert draft_burger.get_receipt() == expected
