import csv
import os
import shutil
import unittest.mock
import json
from unittest import mock
from checkout_and_payment import checkoutAndPayment, ShoppingCart, Product
from checkout_and_payment import check_cart, checkout, User, Product, ShoppingCart
import pytest


class Test_checkcart:
    @pytest.fixture
    def checkout_stub1(self, mocker):
        return mocker.patch('checkout_and_payment.checkout', return_value=None)

    @pytest.fixture
    def new_cart(self):
        return ShoppingCart()
    def test_EC1(self, monkeypatch, new_cart, checkout_stub1):
        product_list = [Product(name='Orange', price=10, units=3)]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name="Kim", wallet='100')

        new_cart.add_item(product_list[0])

        with unittest.mock.patch('builtins.input', return_value='n'):
            result = check_cart(user, new_cart)
        assert result == False
        checkout_stub1.assert_not_called()

    # Test with product in cart, checkout
    def test_EC2(self, checkout_stub1, new_cart, monkeypatch):
        product_list = [Product(name='Orange', price=10, units=3)]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name="Kim", wallet='100')

        new_cart.add_item(product_list[0])

        monkeypatch.setattr('builtins.input', lambda _: 'y')

        result = check_cart(user, new_cart)

        assert result == None
        checkout_stub1.assert_called_once_with(user, new_cart)

    # Test with an empty cart, no checkout
    def test_EC7(self, checkout_stub1, new_cart, monkeypatch):
        user = User(name="Kim", wallet='100')
        monkeypatch.setattr('builtins.input', lambda _: 'n')
        result = check_cart(user, new_cart)

        assert result == False
        checkout_stub1.assert_not_called()

    # Test with negative product price
    def test_EC9(self, checkout_stub1, new_cart, monkeypatch):
        # Negative price products
        product_list = [Product(name='Orange', price=-10, units=3)]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name="Kim", wallet='100')

        new_cart.add_item(product_list[0])

        monkeypatch.setattr('builtins.input', lambda _: 'y')
        result = check_cart(user, new_cart)

        assert result == None
        checkout_stub1.assert_called_once_with(user, new_cart)

    # Test with negative product units
    def test_EC10(self, checkout_stub1, new_cart, monkeypatch):
        # Negative units
        product_list = [Product(name='Orange', price=10, units=-1)]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name="Kim", wallet='100')

        new_cart.add_item(product_list[0])

        monkeypatch.setattr('builtins.input', lambda _: 'y')
        result = check_cart(user, new_cart)

        assert result == None
        checkout_stub1.assert_called_once_with(user, new_cart)

class Test_checkout:
    @pytest.fixture
    def new_cart(self):
        return ShoppingCart()

    # Test with an empty cart
    def test_EC1(self ,capfd, monkeypatch, new_cart):
        product_list = []
        user = User(name='Kim', wallet='20')
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        checkout(user, new_cart)

        captured = capfd.readouterr()

        assert captured.out.strip() == "Your basket is empty. Please add items before checking out."
        assert user.wallet == 20
        assert len(new_cart.retrieve_item()) == 0
        assert len(product_list) == 0

    # Test with not enough money
    def test_EC2(self, capfd, monkeypatch, new_cart):
        product_list = [Product(name='Orange', price=10, units=3)]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name='Kim', wallet=5)
        new_cart.add_item(product_list[0])
        checkout(user, new_cart)

        captured = capfd.readouterr()
        assert captured.out.strip() == f"You don't have enough money to complete the purchase.\nPlease try again!"
        assert user.wallet == 5
        assert len(new_cart.retrieve_item()) == 1
        assert len(product_list) == 1

    # Test with products having negative price
    def test_EC7(self, capfd, monkeypatch, new_cart):
        product_list = [Product(name='Orange', price=-10, units=3)]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name='Kim', wallet=100)

        new_cart.add_item(product_list[0])

        checkout(user, new_cart)

        captured = capfd.readouterr()

        expected_output = f"Thank you for your purchase, {user.name}! Your remaining balance is {user.wallet}"
        assert captured.out.strip() == expected_output

        assert user.wallet == 110
        assert len(new_cart.retrieve_item()) == 0
        assert product_list[0].units == 2

    # Test with wallet having decimal balance
    def test_EC9(self, monkeypatch, new_cart):
        product_list = [Product(name='Orange', price=10, units=3)]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name='Kim', wallet=100.5)
        new_cart.add_item(product_list[0])

        checkout(user, new_cart)

        assert user.wallet == 90.5
        assert len(new_cart.retrieve_item()) == 0
        assert product_list[0].units == 2

    # Test with not enough available units from the start
    def test_EC10(self, monkeypatch, new_cart):
        product_list = [Product(name='Orange', price=10, units=0)]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name='Kim', wallet=100)

        new_cart.add_item(product_list[0])

        checkout(user, new_cart)

        assert user.wallet == 90
        assert len(new_cart.retrieve_item()) == 0
        assert product_list[0].units == -1


class Test_checkout_and_payment:
    @pytest.fixture
    def json_dump_mock(self, monkeypatch):
        # Create a MagicMock for json.dump
        mock_dump = mock.MagicMock()
        monkeypatch.setattr('json.dump', mock_dump)
        return mock_dump

    @pytest.fixture
    def registered_user(self):
        return {"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100}

    @pytest.fixture
    def open_users_file_stub(self, monkeypatch, registered_user):
        # Provide user file content for the login function
        read_data = json.dumps([registered_user])
        monkeypatch.setattr('builtins.open', mock.mock_open(read_data=read_data))

    @pytest.fixture(scope='module')
    def copy_json_file(self):
        shutil.copy('users.json', 'copy_users.json')
        print("-----------------setup------------------")
        yield
        os.remove('copy_users.json')
        print("----------------teardown----------------")

    @pytest.fixture
    def logout_stub1(self, mocker):
        return mocker.patch('logout.logout', return_value=True)

    def mimic_input(self, input_lst):
        i = 0

        def _mimic_input(some_input):
            nonlocal i
            mimicked_input = input_lst[i]
            i += 1
            return mimicked_input

        return _mimic_input

    def test_logout_nonempty_cart(self, capsys, monkeypatch):
        def logout_stub3(cart):
            for item in cart.retrieve_item():
                p = item.get_product()
                logout_cart.append(p)
            return True

        logout_cart = []
        cart = ShoppingCart()
        login_info = {"username": "Ramanathan", "wallet": 100}
        products = [Product("Ice cream", 10, 2)]
        monkeypatch.setattr("checkout_and_payment.cart", cart)
        monkeypatch.setattr("checkout_and_payment.products", products)
        monkeypatch.setattr("builtins.input", mimic_input(["1", "l", "y"]))
        monkeypatch.setattr("checkout_and_payment.logout", logout_stub3)
        checkoutAndPayment(login_info)
        out, err = capsys.readouterr()  # just to get rid of outputs
        assert logout_cart == [['Ice cream', 10.0, 2]]
        assert out[62:-1] == "You have been logged out"

    def test_call_for_dump(self, json_dump_mock, open_users_file_stub, logout_stub1, capsys, monkeypatch):
        def check_cart_stub4(user, cart):
            price = cart.get_total_price()
            user.wallet -= price
            cart.items = []
            return None

        cart = ShoppingCart()
        login_info = {"username": "Ramanathan", "wallet": 100}
        monkeypatch.setattr("checkout_and_payment.cart", cart)
        monkeypatch.setattr("checkout_and_payment.products", [])
        monkeypatch.setattr("builtins.input", mimic_input(["c", "l"]))
        monkeypatch.setattr("checkout_and_payment.logout", logout_stub1)
        monkeypatch.setattr("checkout_and_payment.check_cart", check_cart_stub4)
        checkoutAndPayment(login_info)
        out, err = capsys.readouterr()  # just to get rid of outputs
        json_dump_mock.assert_called_once()

    def test_nonupdated_wallet_after_logout(self, json_dump_mock, open_users_file_stub, logout_stub1, capsys, monkeypatch):
        def check_cart_stub4(user, cart):
            price = cart.get_total_price()
            user.wallet -= price
            cart.items = []
            return None

        cart = ShoppingCart()
        login_info = {"username": "Ramanathan", "wallet": 100}
        monkeypatch.setattr("checkout_and_payment.cart", cart)
        monkeypatch.setattr("checkout_and_payment.products", [])
        monkeypatch.setattr("builtins.input", mimic_input(["c", "l"]))
        monkeypatch.setattr("checkout_and_payment.logout", logout_stub1)
        monkeypatch.setattr("checkout_and_payment.check_cart", check_cart_stub4)
        checkoutAndPayment(login_info)
        out, err = capsys.readouterr()  # just to get rid of outputs
        json_dump_mock.assert_called_once_with(
            [{"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100}], mock.ANY)

    def test_updated_wallet_one_purcase(self, json_dump_mock, open_users_file_stub, logout_stub1, capsys, monkeypatch):
        def check_cart_stub4(user, cart):
            price = cart.get_total_price()
            user.wallet -= price
            cart.items = []
            return None

        cart = ShoppingCart()
        login_info = {"username": "Ramanathan", "wallet": 100}
        products = [Product("Ice cream", 10, 2)]
        monkeypatch.setattr("checkout_and_payment.cart", cart)
        monkeypatch.setattr("checkout_and_payment.products", products)
        monkeypatch.setattr("builtins.input", mimic_input(["1", "c", "l"]))
        monkeypatch.setattr("checkout_and_payment.logout", logout_stub1)
        monkeypatch.setattr("checkout_and_payment.check_cart", check_cart_stub4)
        checkoutAndPayment(login_info)
        out, err = capsys.readouterr()  # just to get rid of outputs
        json_dump_mock.assert_called_once_with([{"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 90}],
                                               mock.ANY)

    def test_updated_wallet_multiple_purcases(self, json_dump_mock, open_users_file_stub, logout_stub1, capsys, monkeypatch):
        def check_cart_stub4(user, cart):
            price = cart.get_total_price()
            user.wallet -= price
            cart.items = []
            return None

        cart = ShoppingCart()
        login_info = {"username": "Ramanathan", "wallet": 100}
        products = [Product("Ice cream", 10, 2), Product("Chocolate", 15, 5), Product("Popcorns", 8, 3)]
        monkeypatch.setattr("checkout_and_payment.cart", cart)
        monkeypatch.setattr("checkout_and_payment.products", products)
        monkeypatch.setattr("builtins.input", mimic_input(["1", "2", "3", "c", "l"]))
        monkeypatch.setattr("checkout_and_payment.logout", logout_stub1)
        monkeypatch.setattr("checkout_and_payment.check_cart", check_cart_stub4)
        checkoutAndPayment(login_info)
        out, err = capsys.readouterr()  # just to get rid of outputs
        json_dump_mock.assert_called_once_with([{"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 67}],
                                               mock.ANY)