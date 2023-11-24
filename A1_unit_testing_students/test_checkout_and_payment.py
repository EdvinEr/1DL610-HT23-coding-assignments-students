from checkout_and_payment import checkoutAndPayment, ShoppingCart, Product
from logout import logout
import pytest
import shutil
import os
import json
from unittest import mock

@pytest.fixture
def json_dump_mock(monkeypatch):
    # Create a MagicMock for json.dump
    mock_dump = mock.MagicMock()
    monkeypatch.setattr('json.dump', mock_dump)
    return mock_dump

@pytest.fixture
def registered_user():
    return {"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100}

@pytest.fixture
def open_users_file_stub(monkeypatch, registered_user):
    # Provide user file content for the login function
    read_data = json.dumps([registered_user])
    monkeypatch.setattr('builtins.open', mock.mock_open(read_data=read_data))

@pytest.fixture(scope='module')
def copy_json_file():
    shutil.copy('users.json', 'copy_users.json')
    print("-----------------setup------------------")
    yield
    os.remove('copy_users.json')
    print("----------------teardown----------------")

@pytest.fixture
def logout_stub1(mocker):
    return mocker.patch('logout.logout', return_value=True)

def mimic_input(input_lst):
    i = 0

    def _mimic_input(some_input):
        nonlocal i
        mimicked_input = input_lst[i]
        i += 1
        return mimicked_input
    return _mimic_input

#=============================== Printout testing ====================================
def test_printout_logout_confirmed(logout_stub1, capsys, monkeypatch):
    login_info = {"username": "Ramanathan", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", mimic_input(["l"]))
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()
    expected_output = "You have been logged out"
    assert expected_output in out[:28]

def test_printout_one_product(logout_stub1, capsys, monkeypatch):
    login_info = {"username": "Ramanathan", "wallet": 100}
    products = [Product("Ice cream", 10, 2)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", mimic_input(["l"]))
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()
    expected_o = "1. Ice cream - $10.0 - Units: 2"
    assert expected_o in out[:31]

def test_printout_multiple_products(logout_stub1, capsys, monkeypatch):
    login_info = {"username": "Ramanathan", "wallet": 100}
    products = [Product("Ice cream", 10, 2), Product("Chocolate", 15, 5), Product("Popcorns", 8, 3)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", mimic_input(["l"]))
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()
    expected_o = "1. Ice cream - $10.0 - Units: 2\n2. Chocolate - $15.0 - Units: 5\n3. Popcorns - $8.0 - Units: 3"
    assert expected_o in out[:96]

def test_printout_add_item_to_cart(logout_stub1, capsys, monkeypatch):
    login_info = {"username": "Ramanathan", "wallet": 100}
    cart = ShoppingCart()
    products = [Product("Ice cream", 10, 2)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("builtins.input", mimic_input(["1", "l", "y"]))
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()
    expected_output = "Ice cream added to your cart."
    assert expected_output in out[30:]

def test_printout_item_out_of_stock(logout_stub1, capsys, monkeypatch):
    login_info = {"username": "Ramanathan", "wallet": 100}
    cart = ShoppingCart()
    products = [Product("Ice cream", 10, 0)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("builtins.input", mimic_input(["1", "l", "y"]))
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()
    expected_output = "Sorry, Ice cream is out of stock."
    assert expected_output in out[30:]

def test_printout_choice_other_letter(logout_stub1, capsys, monkeypatch):
    login_info = {"username": "Ramanathan", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", mimic_input(["a", "l"]))
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()
    expected_output = "Invalid input. Please try again."
    assert expected_output in out

def test_printout_choice_other_number(capsys, monkeypatch):
    login_info = {"username": "Ramanathan", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", mimic_input(["5", "l"]))
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()
    expected_output = "Invalid input. Please try again."
    assert expected_output in out


#=============================== Functionality testing ====================================
def test_check_cart_empty_cart(logout_stub1, capsys, monkeypatch):
    def check_cart_stub1(user, cart):
        check_cart.append(cart.retrieve_item())
        return False

    check_cart = []
    cart = ShoppingCart()
    login_info = {"username": "Ramanathan", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", mimic_input(["c", "l"]))

    monkeypatch.setattr("checkout_and_payment.check_cart", check_cart_stub1)
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()  # just to get rid of outputs
    assert check_cart == [[]]

def test_check_cart_nonempty_cart(logout_stub1, capsys, monkeypatch):
    def check_cart_stub2(user, cart):
        for item in cart.retrieve_item():
            p = item.get_product()
            check_cart.append(p)
        return True

    check_cart = []
    cart = ShoppingCart()
    products = [Product("Ice cream", 10, 2)]
    login_info = {"username": "Ramanathan", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", mimic_input(["1", "c", "l", "y"]))
    monkeypatch.setattr("checkout_and_payment.check_cart", check_cart_stub2)
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()  # just to get rid of outputs
    assert check_cart == [['Ice cream', 10.0, 2]]

def test_check_cart_user_info(logout_stub1, capsys, monkeypatch):
    def check_cart_stub3(user, cart):
        check_user.append(user.name)
        check_user.append(user.wallet)
        return False

    check_user = []
    login_info = {"username": "Ramanathan", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", mimic_input(["c", "l"]))
    monkeypatch.setattr("checkout_and_payment.check_cart", check_cart_stub3)
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()  # just to get rid of outputs
    assert check_user[0] == "Ramanathan"
    assert check_user[1] == 100

def test_logout_empty_cart(capsys,monkeypatch):
    def logout_stub2(cart):
        logout_cart.append(cart.retrieve_item())
        return True

    logout_cart = []
    login_info = {"username": "Ramanathan", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", mimic_input(["l"]))
    monkeypatch.setattr("checkout_and_payment.logout", logout_stub2)
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()
    assert logout_cart == [[]]
    assert out[:-1] == "You have been logged out"

def test_logout_nonempty_cart(capsys, monkeypatch):
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
    monkeypatch.setattr("builtins.input", mimic_input(["1","l","y"]))
    monkeypatch.setattr("checkout_and_payment.logout", logout_stub3)
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()      #just to get rid of outputs
    assert logout_cart == [['Ice cream', 10.0, 2]]
    assert out[62:-1] == "You have been logged out"

def test_call_for_dump(json_dump_mock, open_users_file_stub, logout_stub1, capsys, monkeypatch):

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
    out, err = capsys.readouterr()      #just to get rid of outputs
    json_dump_mock.assert_called_once()

def test_nonupdated_wallet_after_logout(json_dump_mock, open_users_file_stub, logout_stub1, capsys, monkeypatch):
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
    out, err = capsys.readouterr()      #just to get rid of outputs
    json_dump_mock.assert_called_once_with([{"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100}], mock.ANY)

def test_updated_wallet_one_purcase(json_dump_mock, open_users_file_stub, logout_stub1, capsys, monkeypatch):
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
    out, err = capsys.readouterr()      #just to get rid of outputs
    json_dump_mock.assert_called_once_with([{"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 90}], mock.ANY)

def test_updated_wallet_multiple_purcases(json_dump_mock, open_users_file_stub, logout_stub1, capsys, monkeypatch):
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
    monkeypatch.setattr("builtins.input", mimic_input(["1","2","3", "c", "l"]))
    monkeypatch.setattr("checkout_and_payment.logout", logout_stub1)
    monkeypatch.setattr("checkout_and_payment.check_cart", check_cart_stub4)
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()      #just to get rid of outputs
    json_dump_mock.assert_called_once_with([{"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 67}], mock.ANY)