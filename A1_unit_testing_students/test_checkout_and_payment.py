from checkout_and_payment import checkoutAndPayment, ShoppingCart, Product
from logout import logout
import pytest
import shutil
import os

@pytest.fixture(scope='module')
def copy_json_file():
    shutil.copy('users.json', 'copy_user.json')
    print("-----------------setup------------------")
    yield
    os.remove('copy_users.json')
    print("----------------teardown----------------")

@pytest.fixture
def check_cart_stub1(mocker):
    return mocker.patch('checkout_and_payment.check_cart', return_value=False)

@pytest.fixture
def check_cart_stub2(mocker):
    return mocker.patch('checkout_and_payment.check_cart', return_value=None)

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
    monkeypatch.setattr("builtins.input", mimic_input(["a", "l"]))
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()
    expected_output = "Invalid input. Please try again."
    assert expected_output in out[2217:2249]

def test_printout_choice_other_number(capsys, monkeypatch):
    login_info = {"username": "Ramanathan", "wallet": 100}
    monkeypatch.setattr("builtins.input", mimic_input(["72", "l"]))
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()
    expected_output = "Invalid input. Please try again."
    assert expected_output in out[2217:2249]





def test_check_cart_empty_cart(logout_stub1, capsys, monkeypatch):
    def check_cart_stub3(user, cart):
        check_cart.append(cart.retrieve_item())
        return False

    check_cart = []
    cart = ShoppingCart()
    login_info = {"username": "Ramanathan", "wallet": 100}
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("checkout_and_payment.products", [])
    monkeypatch.setattr("builtins.input", mimic_input(["c", "l"]))

    monkeypatch.setattr("checkout_and_payment.check_cart", check_cart_stub3)
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()  # just to get rid of outputs
    assert check_cart == [[]]


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
    product = []
    monkeypatch.setattr("checkout_and_payment.products", product)
    monkeypatch.setattr("builtins.input", mimic_input(["l"]))
    monkeypatch.setattr("checkout_and_payment.logout", logout_stub2)
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()      #just to get rid of outputs
    assert logout_cart == [[]]

def test_logout_nonempty_cart(capsys, monkeypatch):
    def logout_stub2(cart):
        for item in cart.retrieve_item():
            p = item.get_product()
            logout_cart.append(p)
        return True

    logout_cart = []
    cart = ShoppingCart()
    login_info = {"username": "Ramanathan", "wallet": 100}
    product = [Product("Ice cream", 10, 2)]
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("checkout_and_payment.products", product)
    monkeypatch.setattr("builtins.input", mimic_input(["1","l","y"]))
    monkeypatch.setattr("checkout_and_payment.logout", logout_stub2)
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()      #just to get rid of outputs
    assert logout_cart == [['Ice cream', 10.0, 2]]