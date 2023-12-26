import pytest
from unittest.mock import patch, MagicMock, mock_open
from products import searchAndBuyProduct
import json


@pytest.fixture
def json_dump_mock(monkeypatch):
    # Create a MagicMock for json.dump
    mock_dump = MagicMock()
    monkeypatch.setattr('json.dump', mock_dump)
    return mock_dump


@pytest.fixture
def registered_user():
    return {"username": "testuser", "password": "Test_Password", "wallet": 100}


@pytest.fixture
def login_open_users_file_stub(monkeypatch, registered_user):
    # Provide user file content for the login function
    read_data = json.dumps([registered_user])
    monkeypatch.setattr('builtins.open', mock_open(read_data=read_data))

@pytest.fixture
def checkoutAndPayment_stub(mocker):
    return mocker.patch('products.checkoutAndPayment', return_value=None)

@pytest.fixture
def display_csv_as_table_stub(mocker):
    return mocker.patch('products.display_csv_as_table', return_value=None)

@pytest.fixture
def display_filtered_table_stub(mocker):
    return mocker.patch('products.display_filtered_table', return_value=None)

### Check for successful login and a single search to work properly

@pytest.mark.parametrize("user_inputs", [("testuser", "Test_Password", "all", "Y")])
def test_with_login_successful_and_search_all(capsys, login_open_users_file_stub, json_dump_mock,
                     checkoutAndPayment_stub, display_csv_as_table_stub,
                     display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the output contains the expected message
    assert "Successfully logged in" in captured.out

    display_csv_as_table_stub.assert_called_once()
    display_filtered_table_stub.assert_not_called()
    checkoutAndPayment_stub.assert_called_once_with({"username": "testuser", "wallet": 100 })

@pytest.mark.parametrize("user_inputs", [("testuser", "Test_Password", "Apple", "Y")])
def test_with_login_successful_and_search_one_product(capsys, login_open_users_file_stub, json_dump_mock,
                     checkoutAndPayment_stub, display_csv_as_table_stub,
                     display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the output contains the expected message
    assert "Successfully logged in" in captured.out

    display_csv_as_table_stub.assert_not_called()
    display_filtered_table_stub.assert_called_once()
    checkoutAndPayment_stub.assert_called_once_with({"username": "testuser", "wallet": 100 })

### Check for searches to work properly

@pytest.mark.parametrize("user_inputs", [
    ("testuser", "Test_Password", "Apple", "N", "all", "Y")
])
def test_with_login_successful_and_multiple_searches1(
        capsys, login_open_users_file_stub, json_dump_mock,
        checkoutAndPayment_stub, display_csv_as_table_stub,
        display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the output contains the expected message
    assert "Successfully logged in" in captured.out

    display_csv_as_table_stub.assert_called_once()
    display_filtered_table_stub.assert_called_once()
    checkoutAndPayment_stub.assert_called_once_with({"username": "testuser", "wallet": 100})


@pytest.mark.parametrize("user_inputs", [
    ("testuser", "Test_Password", "Apple", "", "Apple", "Y")
])
def test_with_login_successful_and_multiple_searches2(
        capsys, login_open_users_file_stub, json_dump_mock,
        checkoutAndPayment_stub, display_csv_as_table_stub,
        display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the output contains the expected message
    assert "Successfully logged in" in captured.out

    display_csv_as_table_stub.assert_not_called()
    assert display_filtered_table_stub.call_count == 2
    checkoutAndPayment_stub.assert_called_once_with({"username": "testuser", "wallet": 100})

@pytest.mark.parametrize("user_inputs", [
    ("testuser", "Test_Password", "non_existing_product", "Y"),
    ("testuser", "Test_Password", "", "Y")
])
def test_with_login_successful_and_wrong_search(
        capsys, login_open_users_file_stub, json_dump_mock,
        checkoutAndPayment_stub, display_csv_as_table_stub,
        display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the output contains the expected message
    assert "Successfully logged in" in captured.out

    display_csv_as_table_stub.assert_not_called()
    display_filtered_table_stub.assert_called_once()
    checkoutAndPayment_stub.assert_called_once_with({"username": "testuser", "wallet": 100 })


### Check for login part to work properly

@pytest.mark.parametrize("user_inputs", [
    ("testuser", "wrong-password", "testuser", "Test_Password", "all", "Y")
])
def test_with_login_unsuccessful(capsys, login_open_users_file_stub, json_dump_mock,
                     checkoutAndPayment_stub, display_csv_as_table_stub,
                     display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the output contains the expected message
    assert "Either username or password were incorrect" in captured.out
    assert "Successfully logged in" in captured.out

    display_csv_as_table_stub.assert_called_once()
    display_filtered_table_stub.assert_not_called()
    checkoutAndPayment_stub.assert_called_once_with({"username": "testuser", "wallet": 100 })


@pytest.mark.parametrize("user_inputs", [
    ("non_existing_user", "wrongpassword", "N", "non_existing_user", "wrongpassword", "Y", "Correct_New_Password", "all", "Y")
])
def test_with_login_non_existing_username_and_not_register_at_first(
        capsys, login_open_users_file_stub, json_dump_mock,
        checkoutAndPayment_stub, display_csv_as_table_stub,
        display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the output contains the expected message
    assert "Username does not exists." in captured.out
    assert "Successfully registered" in captured.out

    display_csv_as_table_stub.assert_called_once()
    display_filtered_table_stub.assert_not_called()
    checkoutAndPayment_stub.assert_called_once_with({"username": "non_existing_user", "wallet": 0 })

@pytest.mark.parametrize("user_inputs", [
    ("non_existing_user", "wrongpassword", "Y", "password_missing_capital_letter", "Correct_New_Password", "all", "Y"),
    ("non_existing_user", "wrongpassword", "Y", "PasswordMissingSpecialCharacter", "Correct_New_Password", "all", "Y"),
    ("non_existing_user", "wrongpassword", "Y", "7L%tter", "Correct_New_Password", "all", "Y")
])
def test_with_login_non_existing_username_and_register_with_wrong_password(
        capsys, login_open_users_file_stub, json_dump_mock,
        checkoutAndPayment_stub, display_csv_as_table_stub,
        display_filtered_table_stub, user_inputs):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the output contains the expected message
    assert "Username does not exists." in captured.out
    assert "Password must have at least 1 capital letter, 1 special symbol and be 8 characters long." in captured.out
    assert "Successfully registered" in captured.out

    display_csv_as_table_stub.assert_called_once()
    display_filtered_table_stub.assert_not_called()
    checkoutAndPayment_stub.assert_called_once_with({"username": "non_existing_user", "wallet": 0 })

### Check for other cases to work properly

def test_with_wrong_number_of_userinputs(
        capsys, login_open_users_file_stub, json_dump_mock,
        checkoutAndPayment_stub, display_csv_as_table_stub,
        display_filtered_table_stub):
    i = [0]
    def input_side_effect(prompt):
        i[0] += 1
        if i[0] == 5:
            raise SystemExit
        elif "Enter your username:" in prompt:
            return "testuser"
        elif "Enter your password:" in prompt:
            return "Test_Password"
        elif "Search for products" in prompt:
            return "all"
        elif "Ready to shop" in prompt:
            return "N"
        else:
            return

    with patch('builtins.input', side_effect=input_side_effect):
        with pytest.raises(SystemExit):
            searchAndBuyProduct()

    # Capture the printed output
    captured = capsys.readouterr()

    # Assert the output contains the expected message
    assert "Successfully logged in" in captured.out

    display_csv_as_table_stub.assert_called_once()
    checkoutAndPayment_stub.assert_not_called()


