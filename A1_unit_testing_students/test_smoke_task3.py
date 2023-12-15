import csv, os, shutil, pytest, json, unittest, copy
from unittest import mock
from unittest.mock import patch
from checkout_and_payment import check_cart, checkout, User, Product, ShoppingCart, checkoutAndPayment, load_products_from_csv, change_user_info
from logout import logout
from login import login
from products import display_csv_as_table, display_filtered_table, searchAndBuyProduct

@pytest.fixture()
def copy_new_json_file(scope='function'):
    shutil.copy('users_new.json', 'copy_users_new.json')
    print("-----------------setup------------------")
    yield
    os.remove('copy_users_new.json')
    print("----------------teardown----------------")

# Successful login of existing user
# Correct prints in search products for 'all'
# Ready to shop
# Update the address successfully
# Update the phone number successfully
# Update the email address successfully
# Successfully log out
@pytest.mark.parametrize("user_inputs", [("Ramanathan", "Notaproblem23*", "all", "y", "e", "1", "new_address", "2", "123", "3", "new.email@example.com", "s", "l")])
def test_smoke1(user_inputs, copy_new_json_file, capsys):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct("copy_users_new.json")

    out, err = capsys.readouterr()

    expected_output = "Successfully logged in"
    assert expected_output in out

    expected_output = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
    assert expected_output in out
    expected_output = "['Backpack', '15', '1']"
    assert expected_output in out

    with open("copy_users_new.json", 'r') as json_file:
        users_data = json.load(json_file)

    user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Ramanathan"), None)

    assert users_data[user_index]["address"] == "new_address"
    assert users_data[user_index]["phone_number"] == "123"
    assert users_data[user_index]["email_address"] == "new.email@example.com"

    expected_output = "You have been logged out"
    assert expected_output in out


# Successful login of existing user
# Correct prints in search products for 'Apple'
# Ready to shop
# Edit profile changes nothing
# Successfully log out
@pytest.mark.parametrize("user_inputs", [("Ramanathan", "Notaproblem23*", "Apple", "y", "e", "s", "l")])
def test_smoke2(user_inputs, copy_new_json_file, capsys):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct("copy_users_new.json")

    out, err = capsys.readouterr()

    expected_output = "Successfully logged in"
    assert expected_output in out

    expected_output = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
    assert expected_output in out
    expected_output = "['Backpack', '15', '1']"
    assert expected_output not in out

    with open("copy_users_new.json", 'r') as json_file:
        users_data = json.load(json_file)

    user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Ramanathan"), None)

    assert users_data[user_index]["address"] == "123 Main St, Cityville, USA"
    assert users_data[user_index]["phone_number"] == "+1 (555) 123-4567"
    assert users_data[user_index]["email_address"] == "ramanathan@example.com"

    expected_output = "You have been logged out"
    assert expected_output in out


# Unsuccessful login of existing user, then successful login
# Correct prints in search products for 'Apple'
# Not ready to shop
# Correct prints in search products for 'all'
# Ready to shop
# Edit profile changes address
# Successfully log out
@pytest.mark.parametrize("user_inputs", [("Ramanathan", "Notaproblem", "Ramanathan", "Notaproblem23*", "Apple", "n", "all", "y", "e", "1", "new_address3", "s", "l")])
def test_smoke3(user_inputs, copy_new_json_file, capsys):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct("copy_users_new.json")

    out, err = capsys.readouterr()

    expected_output = "Successfully logged in"
    assert expected_output in out

    expected_output = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
    assert expected_output in out
    expected_output = "['Backpack', '15', '1']"
    assert expected_output in out

    with open("copy_users_new.json", 'r') as json_file:
        users_data = json.load(json_file)

    user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Ramanathan"), None)

    assert users_data[user_index]["address"] == "new_address3"
    assert users_data[user_index]["phone_number"] == "+1 (555) 123-4567"
    assert users_data[user_index]["email_address"] == "ramanathan@example.com"

    expected_output = "You have been logged out"
    assert expected_output in out


# Successful register of new user
# Correct prints in search products for 'all'
# Ready to shop
# Edit profile without updating anything
# Successfully log out
@pytest.mark.parametrize("user_inputs", [("Ram", "Notaproblem", "y", "Notaproblem23*", "new_address4", "new_phone4", "new_mail4", "1234 5678 1234 5678", "4/4", "Ram", "111", "Ram", "Notaproblem23*", "all", "y", "e", "s", "l")])
def test_smoke4(user_inputs, copy_new_json_file, capsys):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct("copy_users_new.json")

    out, err = capsys.readouterr()

    expected_output = "Successfully logged in"
    assert expected_output in out

    expected_output = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
    assert expected_output in out
    expected_output = "['Backpack', '15', '1']"
    assert expected_output in out

    with open("copy_users_new.json", 'r') as json_file:
        users_data = json.load(json_file)

    user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Ram"), None)

    assert users_data[user_index]["address"] == "new_address4"
    assert users_data[user_index]["phone_number"] == "new_phone4"
    assert users_data[user_index]["email_address"] == "new_mail4"
    assert users_data[user_index]["credit_cards"][0]["card_number"] == "1234 5678 1234 5678"
    assert users_data[user_index]["credit_cards"][0]["expiry_date"] == "4/4"
    assert users_data[user_index]["credit_cards"][0]["name_on_card"] == "Ram"
    assert users_data[user_index]["credit_cards"][0]["cvv"] == "111"


    expected_output = "You have been logged out"
    assert expected_output in out


# Wrong username, then successful log in
# Correct prints in search products for 'not_exist'
# Not ready to shop
# Correct prints in search products for 'Backpack'
# Ready to shop
# Succesfully purchase Backpack
# Successfully update email address
# Add apple to cart
# Successfully log out without checkout with apple
@pytest.mark.parametrize("user_inputs", [("Ram", "Notaproblem23*", "n", "Ramanathan", "Notaproblem23*", "not_exist", "n", "Backpack", "y", "71", "c", "y", "e", "3", "ramanathan_new@example.com", "s", "1", "l", "y")])
def test_smoke5(user_inputs, copy_new_json_file, capsys):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct("copy_users_new.json")

    out, err = capsys.readouterr()

    expected_output = "Username does not exists."
    assert expected_output in out
    expected_output = "Successfully logged in"
    assert expected_output in out

    expected_output = "['Product', 'Price', 'Units']\n['Backpack', '25', '1']\n['Backpack', '15', '1']"
    assert expected_output in out
    expected_output = "['Apple', '2', '10']"
    assert expected_output not in out

    with open("copy_users_new.json", 'r') as json_file:
        users_data = json.load(json_file)

    user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Ramanathan"), None)

    assert users_data[user_index]["email_address"] == "ramanathan_new@example.com"
    assert users_data[user_index]["wallet"] == 85.0

    expected_output = "Your cart is not empty.You have following items\n['Apple', 2.0, 10]"
    assert expected_output in out
    expected_output = "You have been logged out"
    assert expected_output in out


# Successful register of new user, but fail first password requirement
# Successful log in of another user
# Correct prints in search products for 'all'
# Ready to shop
# Update credit card information on different cards
# Successfully purchase Apple
# Successfully log out
@pytest.mark.parametrize("user_inputs", [("Ram", "Notaproblem", "y", "Notaproblem", "Notaproblem23*", "new_address6", "new_phone6", "new_mail6", "1234 5678 1234 5678", "6/6", "Ram", "111", "Ramanathan", "Notaproblem23*", "all", "y", "e", "4", "2", "c", "4", "1", "1","1111 2222 1111 2222", "4", "1", "2", "24/12", "4", "2", "3", "Santa", "4", "2", "4", "321", "s", "l")])
def test_smoke6(user_inputs, copy_new_json_file, capsys):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct("copy_users_new.json")

    out, err = capsys.readouterr()

    expected_output = "Password must have at least 1 capital letter, 1 special symbol and be 8 characters long."
    assert expected_output in out
    expected_output = "Successfully logged in"
    assert expected_output in out

    expected_output = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
    assert expected_output in out
    expected_output = "['Backpack', '15', '1']"
    assert expected_output in out

    with open("copy_users_new.json", 'r') as json_file:
        users_data = json.load(json_file)

    user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Ram"), None)
    assert users_data[user_index]["address"] == "new_address6"
    assert users_data[user_index]["phone_number"] == "new_phone6"
    assert users_data[user_index]["email_address"] == "new_mail6"
    assert users_data[user_index]["credit_cards"][0]["card_number"] == "1234 5678 1234 5678"
    assert users_data[user_index]["credit_cards"][0]["expiry_date"] == "6/6"
    assert users_data[user_index]["credit_cards"][0]["name_on_card"] == "Ram"
    assert users_data[user_index]["credit_cards"][0]["cvv"] == "111"

    user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Ramanathan"), None)
    assert users_data[user_index]["credit_cards"][0]["card_number"] == "1111 2222 1111 2222"
    assert users_data[user_index]["credit_cards"][0]["expiry_date"] == "24/12"
    assert users_data[user_index]["credit_cards"][0]["name_on_card"] == "Ramanathan"
    assert users_data[user_index]["credit_cards"][0]["cvv"] == "123"
    assert users_data[user_index]["credit_cards"][1]["card_number"] == "5222 2222 2222 2222"
    assert users_data[user_index]["credit_cards"][1]["expiry_date"] == "08/24"
    assert users_data[user_index]["credit_cards"][1]["name_on_card"] == "Santa"
    assert users_data[user_index]["credit_cards"][1]["cvv"] == "321"

    expected_output = "You have been logged out"
    assert expected_output in out


# Successful log in
# Correct prints in search products for 'all'
# Ready to shop
# Try to check out empty cart
# Add laptop to cart
# Fail checkout of cart due to insufficient wallet
# Successfully update card number
# Successfully log out without checkout with laptop
@pytest.mark.parametrize("user_inputs", [("Ramanathan", "Notaproblem23*", "all", "y", "c", "y", "52", "l", "n", "c", "y", "e", "4", "3", "2", "1", "1111 1111 1111 1111", "c", "s", "l", "y")])
def test_smoke7(user_inputs, copy_new_json_file, capsys):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct("copy_users_new.json")

    out, err = capsys.readouterr()

    expected_output = "Successfully logged in"
    assert expected_output in out

    expected_output = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
    assert expected_output in out
    expected_output = "['Backpack', '25', '1']\n['Backpack', '15', '1']"
    assert expected_output not in out

    with open("copy_users_new.json", 'r') as json_file:
        users_data = json.load(json_file)

    user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Ramanathan"), None)

    assert users_data[user_index]["credit_cards"][1]["card_number"] == "1111 1111 1111 1111"
    assert users_data[user_index]["wallet"] == 100.0

    expected_output = "Your basket is empty. Please add items before checking out."
    assert expected_output in out
    expected_output = "You don't have enough money to complete the purchase.\nPlease try again!"
    assert expected_output in out
    expected_output = "Invalid choice. Please enter a number between 1 and 4 or 's'."
    assert expected_output in out
    expected_output = "You have been logged out"
    assert expected_output in out


# Successful register and log in of new user
# Correct prints in search products for 'all'
# Ready to shop
# Add pens to cart
# Unsuccessful purchase of pens
# Successfully log out
@pytest.mark.parametrize("user_inputs", [("Ram", "Notaproblem", "y", "Notaproblem23*", "new_address8", "new_phone8", "new_mail8", "1234 5678 1234 5678", "8/8", "Ram", "888", "Ram", "Notaproblem23*", "all", "y", "70", "c", "y", "y", "l", "y")])
def test_smoke8(user_inputs, copy_new_json_file, capsys):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct("copy_users_new.json")

    out, err = capsys.readouterr()

    expected_output = "Username does not exists."
    assert expected_output in out
    expected_output = "Successfully logged in"
    assert expected_output in out

    expected_output = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
    assert expected_output in out
    expected_output = "['Backpack', '15', '1']"
    assert expected_output in out

    with open("copy_users_new.json", 'r') as json_file:
        users_data = json.load(json_file)

    user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Ram"), None)
    assert users_data[user_index]["address"] == "new_address8"
    assert users_data[user_index]["phone_number"] == "new_phone8"
    assert users_data[user_index]["email_address"] == "new_mail8"
    assert users_data[user_index]["credit_cards"][0]["card_number"] == "1234 5678 1234 5678"
    assert users_data[user_index]["credit_cards"][0]["expiry_date"] == "8/8"
    assert users_data[user_index]["credit_cards"][0]["name_on_card"] == "Ram"
    assert users_data[user_index]["credit_cards"][0]["cvv"] == "888"

    expected_output = "Pens added to your cart."
    assert expected_output in out
    expected_output = "You don't have enough money to complete the purchase.\nPlease try again!"
    assert expected_output in out
    expected_output = "Invalid input. Please try again."
    assert expected_output in out
    expected_output = "Your cart is not empty.You have following items\n['Pens', 0.5, 10]"
    assert expected_output in out
    expected_output = "You have been logged out"
    assert expected_output in out


# Successful log in
# Correct prints in search products for 'all'
# Ready to shop
# Add running shoes and dumbbells to cart and successfully purchase
# Add salmon and cheese to cart and successfully purchase
# Add strawberry and apple to cart and unsuccessfully purchase
# Successfully log out
@pytest.mark.parametrize("user_inputs", [("Ramanathan", "Notaproblem23*", "all", "y", "63", "61", "c", "y", "20", "18", "c", "y", "6", "l", "c", "y", "l", "y")])
def test_smoke9(user_inputs, copy_new_json_file, capsys):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct("copy_users_new.json")

    out, err = capsys.readouterr()

    expected_output = "Successfully logged in"
    assert expected_output in out

    expected_output = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
    assert expected_output in out
    expected_output = "['Backpack', '15', '1']"
    assert expected_output in out

    with open("copy_users_new.json", 'r') as json_file:
        users_data = json.load(json_file)

    user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Ramanathan"), None)
    assert users_data[user_index]["wallet"] == 5.0

    expected_output = "You don't have enough money to complete the purchase.\nPlease try again!"
    expected_output = "Your cart is not empty."
    assert expected_output in out
    expected_output = "You have been logged out"
    assert expected_output in out

# Successful log in
# Correct prints in search products for 'all'
# Ready to shop
# Successfully log out
@pytest.mark.parametrize("user_inputs", [("Ramanathan", "Notaproblem23*", "all", "y", "l")])
def test_smoke10(user_inputs, copy_new_json_file, capsys):
    with patch('builtins.input', side_effect=user_inputs):
        searchAndBuyProduct("copy_users_new.json")

    out, err = capsys.readouterr()

    expected_output = "Successfully logged in"
    assert expected_output in out

    expected_output = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
    assert expected_output in out
    expected_output = "['Backpack', '15', '1']"
    assert expected_output in out

    expected_output = "You have been logged out"
    assert expected_output in out