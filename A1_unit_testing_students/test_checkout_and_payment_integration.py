from checkout_and_payment import checkoutAndPayment
import pytest
import json
from unittest import mock

### Logout and select item tests
# 1. Test logout with empty cart (flow: logout)
# 2. Test selecting one existing item and cancel logout (flow: select existing item, cancel logout, logout)
# 3. Test selecting one non-existing item (flow: select non-existing item, logout)
# 4. Test selecting one existing and one non-existing item (flow: select one existing and non-existing item, logout)
# 5. Test selecting multiple existing items (flow: select two existing items, logout)
# 6. Test selecting item out of stock (flow: select two existing items, logout)

### Check cart (and select item, logout) tests
# 7. Test checkout empty cart (flow: check-cart, logout)
# 8. Test checkout cart (and the cancelation of it) with one item and enough money (flow: select item, check-cart, cancel checkout, check-cart, checkout, logout)
# 9. Test checkout cart with multiple items and enough money (flow: select two item, check-cart, logout)
# 10. Test checkout cart with not enough money (flow: select item, check-cart, logout)

@pytest.fixture
def json_dump_mock(monkeypatch):
    # Create a MagicMock for json.dump
    mock_dump = mock.MagicMock()
    monkeypatch.setattr('json.dump', mock_dump)
    return mock_dump


@pytest.fixture
def login_info_mock():
    return {"username": "test_user", "wallet": 100}


@pytest.fixture
def registered_user_mock():
    return {"username": "test_user", "password": "Test_User_Password", "wallet": 100}


@pytest.fixture
def products_mock():
    return "Product,Price,Units\nApple,2,10\nBanana,1,15\nOrange,1.5,0\nGold,200,1"


@pytest.fixture
def open_file_stub(mocker, registered_user_mock, products_mock):
    def open_mock(*args, **kwargs):
        file = args[0]
        if file == "users.json":
            users_data = json.dumps([registered_user_mock])
            return mock.mock_open(read_data=users_data)(*args, **kwargs)
        elif file == "products.csv":
            csv_data = products_mock
            return mock.mock_open(read_data=csv_data)(*args, **kwargs)
        else:
            # If open is called with a different file, use the actual open function
            return mocker.DEFAULT

    mocker.patch('builtins.open', side_effect=open_mock)


@pytest.mark.parametrize("user_inputs", ["l"])
def test_logout_with_empty_cart(user_inputs, capsys, open_file_stub, login_info_mock):
    with mock.patch('builtins.input', side_effect=user_inputs):
        checkoutAndPayment(login_info_mock)

    out, err = capsys.readouterr()

    csv_as_table = "1. Apple - $2.0 - Units: 10\n2. Banana - $1.0 - Units: 15\n3. Orange - $1.5 - Units: 0\n4. Gold - $200.0 - Units: 1"
    successful_logout = "You have been logged out"

    assert csv_as_table in out
    assert successful_logout in out


@pytest.mark.parametrize("user_inputs", [("1", "l", "n", "l", "y")])
def test_select_item_and_cancel_logout(user_inputs, capsys, open_file_stub, login_info_mock, json_dump_mock):
    with mock.patch('builtins.input', side_effect=user_inputs):
        checkoutAndPayment(login_info_mock)

    out, err = capsys.readouterr()

    csv_as_table = "1. Apple - $2.0 - Units: 10\n2. Banana - $1.0 - Units: 15\n3. Orange - $1.5 - Units: 0\n4. Gold - $200.0 - Units: 1"
    selected_item_message = "Apple added to your cart."
    non_empty_cart_in_logout = "Your cart is not empty.You have following items\n['Apple', 2.0, 10]"
    successful_logout = "You have been logged out"

    assert out.count(csv_as_table) == 1
    assert out.count(selected_item_message) == 1
    assert out.count(non_empty_cart_in_logout) == 2
    assert out.count(successful_logout) == 1

    json_dump_mock.assert_called_once_with([{"username": "test_user", "password": "Test_User_Password", "wallet": 100}], mock.ANY)


@pytest.mark.parametrize("user_inputs", [("5", "l")])
def test_select_non_existing_item(user_inputs, capsys, open_file_stub, login_info_mock, json_dump_mock):
    with mock.patch('builtins.input', side_effect=user_inputs):
        checkoutAndPayment(login_info_mock)

    out, err = capsys.readouterr()

    csv_as_table = "1. Apple - $2.0 - Units: 10\n2. Banana - $1.0 - Units: 15\n3. Orange - $1.5 - Units: 0\n4. Gold - $200.0 - Units: 1"
    invalid_item_select = "\nInvalid input. Please try again."
    non_empty_cart_in_logout = "Your cart is not empty.You have following items"
    successful_logout = "You have been logged out"

    assert out.count(csv_as_table) == 1
    assert out.count(invalid_item_select) == 1
    assert out.count(non_empty_cart_in_logout) == 0
    assert out.count(successful_logout) == 1

    json_dump_mock.assert_called_once_with([{"username": "test_user", "password": "Test_User_Password", "wallet": 100}], mock.ANY)


@pytest.mark.parametrize("user_inputs", [("1", "5", "l", "y")])
def test_select_existing_and_non_existing_item(user_inputs, capsys, open_file_stub, login_info_mock, json_dump_mock):
    with mock.patch('builtins.input', side_effect=user_inputs):
        checkoutAndPayment(login_info_mock)

    out, err = capsys.readouterr()

    csv_as_table = "1. Apple - $2.0 - Units: 10\n2. Banana - $1.0 - Units: 15\n3. Orange - $1.5 - Units: 0\n4. Gold - $200.0 - Units: 1"
    selected_item_message = "Apple added to your cart."
    invalid_item_select = "\nInvalid input. Please try again."
    non_empty_cart_in_logout = "Your cart is not empty.You have following items\n['Apple', 2.0, 10]"
    successful_logout = "You have been logged out"

    assert out.count(csv_as_table) == 1
    assert out.count(selected_item_message) == 1
    assert out.count(invalid_item_select) == 1
    assert out.count(non_empty_cart_in_logout) == 1
    assert out.count(successful_logout) == 1

    json_dump_mock.assert_called_once_with([{"username": "test_user", "password": "Test_User_Password", "wallet": 100}], mock.ANY)


@pytest.mark.parametrize("user_inputs", [("1", "2", "l", "y")])
def test_select_multiple_item(user_inputs, capsys, open_file_stub, login_info_mock, json_dump_mock):
    with mock.patch('builtins.input', side_effect=user_inputs):
        checkoutAndPayment(login_info_mock)

    out, err = capsys.readouterr()

    csv_as_table = "1. Apple - $2.0 - Units: 10\n2. Banana - $1.0 - Units: 15\n3. Orange - $1.5 - Units: 0\n4. Gold - $200.0 - Units: 1"
    selected_item_message_1 = "Apple added to your cart."
    selected_item_message_2 = "Banana added to your cart."
    non_empty_cart_in_logout = "Your cart is not empty.You have following items\n['Apple', 2.0, 10]\n['Banana', 1.0, 15]"
    successful_logout = "You have been logged out"

    assert out.count(csv_as_table) == 1
    assert out.count(selected_item_message_1) == 1
    assert out.count(selected_item_message_2) == 1
    assert out.count(non_empty_cart_in_logout) == 1
    assert out.count(successful_logout) == 1

    json_dump_mock.assert_called_once_with([{"username": "test_user", "password": "Test_User_Password", "wallet": 100}], mock.ANY)


@pytest.mark.parametrize("user_inputs", [("3", "l")])
def test_select_item_out_of_stock(user_inputs, capsys, open_file_stub, login_info_mock, json_dump_mock):
    with mock.patch('builtins.input', side_effect=user_inputs):
        checkoutAndPayment(login_info_mock)

    out, err = capsys.readouterr()

    csv_as_table = "1. Apple - $2.0 - Units: 10\n2. Banana - $1.0 - Units: 15\n3. Orange - $1.5 - Units: 0\n4. Gold - $200.0 - Units: 1"
    product_out_of_stock = "Sorry, Orange is out of stock."
    non_empty_cart_in_logout = "Your cart is not empty.You have following items"
    successful_logout = "You have been logged out"

    assert out.count(csv_as_table) == 1
    assert out.count(product_out_of_stock) == 1
    assert out.count(non_empty_cart_in_logout) == 0
    assert out.count(successful_logout) == 1

    json_dump_mock.assert_called_once_with([{"username": "test_user", "password": "Test_User_Password", "wallet": 100}], mock.ANY)


@pytest.mark.parametrize("user_inputs", [("c", "y", "l")])
def test_checkout_empty_cart(user_inputs, capsys, open_file_stub, login_info_mock, json_dump_mock):
    with mock.patch('builtins.input', side_effect=user_inputs):
        checkoutAndPayment(login_info_mock)

    out, err = capsys.readouterr()

    csv_as_table = "1. Apple - $2.0 - Units: 10\n2. Banana - $1.0 - Units: 15\n3. Orange - $1.5 - Units: 0\n4. Gold - $200.0 - Units: 1"
    checkout_empty_cart = "Your basket is empty. Please add items before checking out."
    non_empty_cart_in_logout = "Your cart is not empty.You have following items['Apple', 2.0, 10]"
    successful_logout = "You have been logged out"

    assert out.count(csv_as_table) == 1
    assert out.count(checkout_empty_cart) == 1
    assert out.count(non_empty_cart_in_logout) == 0
    assert out.count(successful_logout) == 1

    json_dump_mock.assert_called_once_with([{"username": "test_user", "password": "Test_User_Password", "wallet": 100}], mock.ANY)


@pytest.mark.parametrize("user_inputs", [("1", "c", "n", "c", "y", "l")])
def test_checkout_and_cancel_checkout_cart_with_one_item(user_inputs, capsys, open_file_stub, login_info_mock, json_dump_mock):
    with mock.patch('builtins.input', side_effect=user_inputs):
        checkoutAndPayment(login_info_mock)

    out, err = capsys.readouterr()

    csv_as_table = "1. Apple - $2.0 - Units: 10\n2. Banana - $1.0 - Units: 15\n3. Orange - $1.5 - Units: 0\n4. Gold - $200.0 - Units: 1"
    selected_item_message_1 = "Apple added to your cart."
    check_cart_printout = "['Apple', 2.0, 10]"
    checkout_cart = "Thank you for your purchase, test_user! Your remaining balance is 98.0"
    non_empty_cart_in_logout = "Your cart is not empty.You have following items['Apple', 2.0, 10]"
    successful_logout = "You have been logged out"

    assert out.count(csv_as_table) == 1
    assert out.count(selected_item_message_1) == 1
    assert out.count(check_cart_printout) == 2
    assert out.count(checkout_cart) == 1
    assert out.count(non_empty_cart_in_logout) == 0
    assert out.count(successful_logout) == 1

    json_dump_mock.assert_called_once_with([{"username": "test_user", "password": "Test_User_Password", "wallet": 98}], mock.ANY)


@pytest.mark.parametrize("user_inputs", [("1", "2", "c", "y", "l")])
def test_checkout_multiple_items(user_inputs, capsys, open_file_stub, login_info_mock, json_dump_mock):
    with mock.patch('builtins.input', side_effect=user_inputs):
        checkoutAndPayment(login_info_mock)

    out, err = capsys.readouterr()

    csv_as_table = "1. Apple - $2.0 - Units: 10\n2. Banana - $1.0 - Units: 15\n3. Orange - $1.5 - Units: 0\n4. Gold - $200.0 - Units: 1"
    selected_item_message_1 = "Apple added to your cart."
    selected_item_message_2 = "Banana added to your cart."
    check_cart_printout = "['Apple', 2.0, 10]\n['Banana', 1.0, 15]"
    checkout_cart = "Thank you for your purchase, test_user! Your remaining balance is 97.0"
    non_empty_cart_in_logout = "Your cart is not empty.You have following items"
    successful_logout = "You have been logged out"

    assert out.count(csv_as_table) == 1
    assert out.count(selected_item_message_1) == 1
    assert out.count(selected_item_message_2) == 1
    assert out.count(check_cart_printout) == 1
    assert out.count(checkout_cart) == 1
    assert out.count(non_empty_cart_in_logout) == 0
    assert out.count(successful_logout) == 1

    json_dump_mock.assert_called_once_with([{"username": "test_user", "password": "Test_User_Password", "wallet": 97}], mock.ANY)


@pytest.mark.parametrize("user_inputs", [("4", "c", "y", "l", "y")])
def test_checkout_multiple_items_too_expensive(user_inputs, capsys, open_file_stub, login_info_mock, json_dump_mock):
    with mock.patch('builtins.input', side_effect=user_inputs):
        checkoutAndPayment(login_info_mock)

    out, err = capsys.readouterr()

    csv_as_table = "1. Apple - $2.0 - Units: 10\n2. Banana - $1.0 - Units: 15\n3. Orange - $1.5 - Units: 0\n4. Gold - $200.0 - Units: 1"
    selected_item_message = "Gold added to your cart."
    check_cart_printout = "['Gold', 200.0, 1]"
    checkout_cart_too_expensive = "You don't have enough money to complete the purchase.\nPlease try again!"
    non_empty_cart_in_logout = "Your cart is not empty.You have following items\n['Gold', 200.0, 1]"
    successful_logout = "You have been logged out"

    assert out.count(csv_as_table) == 1
    assert out.count(selected_item_message) == 1
    assert out.count(check_cart_printout) == 2
    assert out.count(checkout_cart_too_expensive) == 1
    assert out.count(non_empty_cart_in_logout) == 1
    assert out.count(successful_logout) == 1

    json_dump_mock.assert_called_once_with([{"username": "test_user", "password": "Test_User_Password", "wallet": 100}], mock.ANY)
