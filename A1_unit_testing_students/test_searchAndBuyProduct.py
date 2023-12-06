import pytest
from unittest.mock import patch
from products import searchAndBuyProduct

@pytest.fixture
def login_stub(mocker):
    return mocker.patch('products.login', return_value={"username": "Ramanathan", "wallet": 100 })

@pytest.fixture
def login_fail_stub(mocker):
    return mocker.patch('products.login', return_value=None, side_effect=[None, None, Exception("Login failed")])

@pytest.fixture
def login_fail_then_succeed_stub(mocker):
    return mocker.patch('products.login', side_effect=[None, {"username": "Ramanathan", "wallet": 100}])

@pytest.fixture
def checkoutAndPayment_stub(mocker):
    return mocker.patch('products.checkoutAndPayment', return_value=None)

@pytest.fixture
def display_csv_as_table_stub(mocker):
    return mocker.patch('products.display_csv_as_table', return_value=None)

@pytest.fixture
def display_filtered_table_stub(mocker):
    return mocker.patch('products.display_filtered_table', return_value=None)

@pytest.mark.parametrize("user_inputs", [("all", "Y")])
def test_with_stubs1(login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    login_stub.assert_called_once()
    display_csv_as_table_stub.assert_called_once()
    display_filtered_table_stub.assert_not_called()
    checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100 })

@pytest.mark.parametrize("user_inputs", [("Apple", "Y")])
def test_with_stubs2(login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    login_stub.assert_called_once()
    display_csv_as_table_stub.assert_not_called()
    display_filtered_table_stub.assert_called_once()
    checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100 })

@pytest.mark.parametrize("user_inputs", [("Apple", "N", "all", "Y")])
def test_with_stubs3(login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    login_stub.assert_called_once()
    display_csv_as_table_stub.assert_called_once()
    display_filtered_table_stub.assert_called_once()
    checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100})

def test_with_stubs4(login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
    i = [0]

    def input_side_effect(prompt):
        i[0] += 1
        if i[0] == 3:
            raise SystemExit
        elif "Search for products" in prompt:
            return "all"
        elif "Ready to shop" in prompt:
            return "N"
        else:
            return

    with patch('builtins.input', side_effect=input_side_effect):
        with pytest.raises(SystemExit):
            searchAndBuyProduct()

    login_stub.assert_called_once()
    display_csv_as_table_stub.assert_called_once()
    checkoutAndPayment_stub.assert_not_called()

@pytest.mark.parametrize("user_inputs", [("all", "Y")])
def test_with_stubs5(login_fail_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        with pytest.raises(Exception, match="Login failed"):
            searchAndBuyProduct()

    assert login_fail_stub.call_count >= 2
    display_csv_as_table_stub.assert_not_called()
    display_filtered_table_stub.assert_not_called()
    checkoutAndPayment_stub.assert_not_called()

@pytest.mark.parametrize("user_inputs", [("all", "Y")])
def test_with_stubs6(login_fail_then_succeed_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    assert login_fail_then_succeed_stub.call_count == 2
    display_csv_as_table_stub.assert_called_once()
    display_filtered_table_stub.assert_not_called()
    checkoutAndPayment_stub.assert_called_once()

@pytest.mark.parametrize("user_inputs", [("Apple", "N", "Apple", "Y")])
def test_with_stubs7(login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    login_stub.assert_called_once()
    display_csv_as_table_stub.assert_not_called()
    assert display_filtered_table_stub.call_count == 2
    checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100})

@pytest.mark.parametrize("user_inputs", [("non_existing_product", "Y")])
def test_with_stubs8(login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    login_stub.assert_called_once()
    display_csv_as_table_stub.assert_not_called()
    display_filtered_table_stub.assert_called_once()
    checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100 })

@pytest.mark.parametrize("user_inputs", [("Apple", "", "all", "Y")])
def test_with_stubs9(login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    login_stub.assert_called_once()
    display_csv_as_table_stub.assert_called_once()
    display_filtered_table_stub.assert_called_once()
    checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100})

@pytest.mark.parametrize("user_inputs", [("", "Y")])
def test_with_stubs10(login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    login_stub.assert_called_once()
    display_csv_as_table_stub.assert_not_called()
    display_filtered_table_stub.assert_called_once()
    checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100})