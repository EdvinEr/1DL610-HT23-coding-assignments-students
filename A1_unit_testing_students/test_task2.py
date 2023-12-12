import csv
import os
import shutil
import unittest.mock
from unittest.mock import patch
import json
from unittest import mock
from checkout_and_payment import checkoutAndPayment, Product, check_cart, checkout, User, ShoppingCart, load_products_from_csv
from products import display_csv_as_table, display_filtered_table, searchAndBuyProduct
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
        json_dump_mock.assert_called_once_with([{"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 67}], mock.ANY)

class Test_display_csv_as_table:
    # Test a non-existing file
    def test_EC1(self):
        with pytest.raises(FileNotFoundError):
            display_csv_as_table("non_existing_file.csv")

    # Test an empty csv file
    def test_EC2(self, capsys):
        display_csv_as_table("test_files/test_empty.csv")
        out, err = capsys.readouterr()
        assert out == ""

    # Test a csv file containing 4 columns
    def test_EC7(self, capsys):
        display_csv_as_table("test_files/test_4_columns.csv")
        out, err = capsys.readouterr()
        assert out[0:39] == "['Product', 'Price', 'Units', 'Status']"
        assert out[40:65] == "['Apple', '2', '10', '1']"
        assert out[66:92] == "['Banana', '1', '15', '0']"
        assert out[93:120] == "['Orange', '1.5', '8', '0']"

    # Test a csv file containing varying column amounts
    def test_EC8(self, capsys):
        display_csv_as_table("test_files/test_different_column_amounts.csv")
        out, err = capsys.readouterr()
        assert out[0:39] == "['Product', 'Price', 'Units', 'Status']"
        assert out[40:49] == "['Apple']"
        assert out[50:65] == "['Banana', '1']"
        assert out[66:88] == "['Orange', '1.5', '8']"

    def test_EC9(self, capsys, copy_csv_file):
        display_csv_as_table("copy_products.csv")
        out, err = capsys.readouterr()
        assert out[0:29] == "['Product', 'Price', 'Units']"
        assert out[30:50] == "['Apple', '2', '10']"
        assert out[51:72] == "['Banana', '1', '15']"
        assert out[73:95] == "['Orange', '1.5', '8']"
        assert out[96:116] == "['Grapes', '3', '5']"


class Test_display_filtered_table:
    # Test a csv file not containing a 'Product' column
    def test_EC10(self):
        with pytest.raises(ValueError):
            display_filtered_table("test_files/test_no_product_column.csv", "Banana")

    # Test a csv file with 'Product' as the second column
    def test_EC11(self, capsys):
        display_filtered_table("test_files/test_product_is_second_column.csv", "Banana")
        out, err = capsys.readouterr()
        assert out == "['Price', 'Product', 'Units']\n['1', 'Banana', '15']\n"

    # Test a csv file containing varying column amounts with 'Product' as the second column
    def test_EC12(self, capsys):
        display_filtered_table("test_files/test_varying_amounts_product_is_second.csv", "Banana")
        out, err = capsys.readouterr()
        assert out == "['Price', 'Product', 'Units']\n['1', 'Banana', '15']\n"

    # Test a non-existing product
    def test_EC13(self, capsys, copy_csv_file):
        display_filtered_table("copy_products.csv", "Pancake")
        out, err = capsys.readouterr()
        assert out == "['Product', 'Price', 'Units']\n"

    def test_EC14a(self, capsys, copy_csv_file):
        display_filtered_table("copy_products.csv", "Apple")
        out, err = capsys.readouterr()
        assert out == "['Product', 'Price', 'Units']\n['Apple', '2', '10']\n"

    def test_EC14b(self, capsys, copy_csv_file):
        display_filtered_table("copy_products.csv", "Dish Soap")
        out, err = capsys.readouterr()
        assert out == "['Product', 'Price', 'Units']\n['Soap', '1', '12']\n['Dish Soap', '1.5', '12']\n"

class Test_load_products_from_csv:
    @pytest.fixture(scope='module')
    def empty_csv_file(self):
        empty_products = 'empty_products.csv'

        with open(empty_products, 'w', newline='') as csvfile:
            fields = ['Product', 'Price', 'Units']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
        products = load_products_from_csv(empty_products)
        print("----------setup----------")
        yield products
        os.remove(empty_products)
        print("----------teardown----------")

    @pytest.fixture(scope='module')
    def modify_csv_file(self):
        shutil.copy('products.csv', 'modify_products.csv')
        yield 'modify_products.csv'
        os.remove('modify_products.csv')

    # Test a non-existing file
    def test_EC1(self):
        with pytest.raises(FileNotFoundError):
            assert load_products_from_csv("non_existing.csv")

    # Test when products have integer or floats as name
    def test_EC7(self, modify_csv_file):
        with open(modify_csv_file, mode='a', newline='') as csvfile:
            fields = ['Product', 'Price', 'Units']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writerow({'Product': 1, 'Price': '3.0', 'Units': '10'})
            writer.writerow({'Product': 0.5, 'Price': '4.0', 'Units': '3'})

        modified_products = load_products_from_csv(modify_csv_file)
        assert modified_products[75].name == '1'
        assert modified_products[76].name == '0.5'

    # Test when CSV file has one less column
    def test_EC9(self, modify_csv_file):
        with open(modify_csv_file, mode='w', newline='') as csvfile:
            fields = ['Product', 'Price']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerow({'Product': 'Cheese', 'Price': '3.0'})

        with pytest.raises(KeyError):
            modified_products = load_products_from_csv(modify_csv_file)

    # Test when CSV file has one more column
    def test_EC10(self, modify_csv_file):
        with open(modify_csv_file, mode='w', newline='') as csvfile:
            fields = ['Product', 'Price', 'Units', 'Category']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerow({'Product': 'Cheese', 'Price': '3.0', 'Units': '4', 'Category': 'Dairy'})
            writer.writerow({'Product': 'Popcorn', 'Price': '4.0', 'Units': '3', 'Category': 'Snacks'})

        modified_products = load_products_from_csv(modify_csv_file)
        assert not any('Dairy' in str(product) for product in modified_products)

    # Test when product has whitespaces in CSV file
    def test_EC11(self, modify_csv_file):
        # CSV file with values with whitespaces
        with open(modify_csv_file, mode='w', newline='') as csvfile:
            fields = ['Product', 'Price', 'Units', 'Category']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerow({'Product': 'Bread ', 'Price': ' 3.0 ', 'Units': ' 6 '})

        modified_products = load_products_from_csv(modify_csv_file)

        assert modified_products[0].name == 'Bread '
        assert modified_products[0].price == 3.0
        assert modified_products[0].units == 6

class Test_searchAndBuyProducts:
    @pytest.fixture
    def login_stub(self, mocker):
        return mocker.patch('products.login', return_value={"username": "Ramanathan", "wallet": 100})

    @pytest.fixture
    def login_fail_stub(self, mocker):
        return mocker.patch('products.login', return_value=None, side_effect=[None, None, Exception("Login failed")])

    @pytest.fixture
    def login_fail_then_succeed_stub(self, mocker):
        return mocker.patch('products.login', side_effect=[None, {"username": "Ramanathan", "wallet": 100}])

    @pytest.fixture
    def checkoutAndPayment_stub(self, mocker):
        return mocker.patch('products.checkoutAndPayment', return_value=None)

    @pytest.fixture
    def display_csv_as_table_stub(self, mocker):
        return mocker.patch('products.display_csv_as_table', return_value=None)

    @pytest.fixture
    def display_filtered_table_stub(self, mocker):
        return mocker.patch('products.display_filtered_table', return_value=None)

    @pytest.mark.parametrize("user_inputs", [("all", "Y")])
    def test_with_stubs1(self, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub,
                         user_inputs):
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct()

        login_stub.assert_called_once()
        display_csv_as_table_stub.assert_called_once()
        display_filtered_table_stub.assert_not_called()
        checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100})

    @pytest.mark.parametrize("user_inputs", [("Apple", "Y")])
    def test_with_stubs2(self, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub,
                         user_inputs):
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct()

        login_stub.assert_called_once()
        display_csv_as_table_stub.assert_not_called()
        display_filtered_table_stub.assert_called_once()
        checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100})

    @pytest.mark.parametrize("user_inputs", [("Apple", "N", "Apple", "Y")])
    def test_with_stubs7(self, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub,
                         user_inputs):
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct()

        login_stub.assert_called_once()
        display_csv_as_table_stub.assert_not_called()
        assert display_filtered_table_stub.call_count == 2
        checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100})

    @pytest.mark.parametrize("user_inputs", [("Apple", "", "all", "Y")])
    def test_with_stubs9(self, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub,
                         user_inputs):
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct()

        login_stub.assert_called_once()
        display_csv_as_table_stub.assert_called_once()
        display_filtered_table_stub.assert_called_once()
        checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100})

    @pytest.mark.parametrize("user_inputs", [("", "Y")])
    def test_with_stubs10(self, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub,
                          user_inputs):
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct()

        login_stub.assert_called_once()
        display_csv_as_table_stub.assert_not_called()
        display_filtered_table_stub.assert_called_once()
        checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100})
