import csv, os, shutil, pytest, json, unittest, copy
from unittest import mock
from unittest.mock import patch
from checkout_and_payment import check_cart, checkout, User, Product, ShoppingCart, checkoutAndPayment, load_products_from_csv, choose_card
from logout import logout
from login import login
from products import display_csv_as_table, display_filtered_table, searchAndBuyProduct

@pytest.fixture(scope='module')
def copy_new_json_file():
    shutil.copy('users_new.json', 'copy_users_new.json')
    yield
    os.remove('copy_users_new.json')


class Test_smoke:
    #Successful Login User exist --> Search products --> Ready to shop --> logout
    @pytest.mark.parametrize("user_inputs", [("Steve", "Steve1", "all", "Y", "l")])
    def test_1(self, capfd, user_inputs, copy_new_json_file):
            with patch('builtins.input', side_effect=user_inputs):
                searchAndBuyProduct('copy_users_new.json')

            captured = capfd.readouterr()
            expected_output_login = "Successfully logged in"
            expected_output_logout = "You have been logged out"
            expected_products = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"

            with open("copy_users_new.json", 'r') as json_file:
                users_data = json.load(json_file)

            user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Steve"), None)

            assert users_data[user_index]["wallet"] == 100.0
            assert expected_output_login in captured.out.strip()
            assert expected_output_logout in captured.out.strip()
            assert expected_products in captured.out.strip()

    @pytest.mark.parametrize("user_inputs", [("Steve", "Steve1", "all", "Y", "c", "y", "l")])
    def test_2(self, capfd, user_inputs, copy_new_json_file):
        # Successful Login User exist --> Search products --> Ready to shop --> Checkcart --> Checkout --> logout
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct('copy_users_new.json')

        with open("copy_users_new.json", 'r') as json_file:
            users_data = json.load(json_file)

        user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Steve"), None)

        assert users_data[user_index]["wallet"] == 100.0

        captured = capfd.readouterr()
        expected_output_login = "Successfully logged in"
        expected_output_logout = "You have been logged out"
        expected_products = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
        expected_output_empty = "Your basket is empty. Please add items before checking out."

        assert expected_output_login in captured.out.strip()
        assert expected_output_logout in captured.out.strip()
        assert expected_products in captured.out.strip()
        assert expected_output_empty in captured.out.strip()


    @pytest.mark.parametrize("user_inputs", [("Steve", "Steve1", "all", "Y", "70", "c", "y", "card", "1", "l")])
    def test_3(self, capfd, user_inputs, copy_new_json_file):
        # Successful Login User exist --> Search products --> Ready to shop --> Add Pen --> Check cart --> Card --> Card 1 --> logout
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct('copy_users_new.json')

        with open("copy_users_new.json", 'r') as json_file:
            users_data = json.load(json_file)

        user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Steve"), None)

        assert users_data[user_index]["wallet"] == 100.0

        captured = capfd.readouterr()

        expected_output_login = "Successfully logged in"
        expected_output_logout = "You have been logged out"
        expected_products = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
        expected_output_choose_card = "Card 1 was chosen."
        expected_output_payment_card = 'Payment successful using card 1'
        expected_output_purchase = "Thank you for your purchase!"

        assert expected_output_login in captured.out.strip()
        assert expected_output_logout in captured.out.strip()
        assert expected_products in captured.out.strip()
        assert expected_output_choose_card in captured.out.strip()
        assert expected_output_payment_card in captured.out.strip()
        assert expected_output_purchase in captured.out.strip()


    @pytest.mark.parametrize("user_inputs", [("Steve", "Steve1", "all", "Y", "71", "c", "y", "wrong", "wallet", "l")])
    def test_4(self, capfd, user_inputs, copy_new_json_file):
        # Successful Login User exist --> Search products --> Ready to shop --> Add Backpack --> Check cart --> Wrong input --> Wallet --> logout
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct('copy_users_new.json')

        with open("copy_users_new.json", 'r') as json_file:
            users_data = json.load(json_file)

        user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Steve"), None)

        assert users_data[user_index]["wallet"] == 85.0

        captured = capfd.readouterr()

        expected_output_login = "Successfully logged in"
        expected_output_logout = "You have been logged out"
        expected_products = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"

        expected_output_payment_method = "Invalid payment method. Please enter 'wallet' or 'card'."
        expected_output_purchase_wallet = "Thank you for your purchase, Steve! Your remaining balance is 85.0"

        assert expected_output_login in captured.out.strip()
        assert expected_output_logout in captured.out.strip()
        assert expected_products in captured.out.strip()
        assert expected_output_payment_method in captured.out.strip()
        assert expected_output_purchase_wallet in captured.out.strip()

    @pytest.mark.parametrize("user_inputs", [("Steve", "Steve1", "x", "n", "all", "y", "69", "70", "c", "n", "c", "y", "card", "2", "l")])
    # Successful Login User exist --> Search products --> Ready to shop --> Add Notebook --> Add Pen --> Check cart -->  Card --> Card 2 --> logout
    def test_5(self, capfd, user_inputs, copy_new_json_file):
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct('copy_users_new.json')

        with open("copy_users_new.json", 'r') as json_file:
            users_data = json.load(json_file)

        user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Steve"), None)

        assert users_data[user_index]["wallet"] == 85.0

        captured = capfd.readouterr()

        expected_output_login = "Successfully logged in"
        expected_output_logout = "You have been logged out"
        expected_products = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
        expected_items_added = "Notebook added to your cart.\nPens added to your cart."

        expected_output_choose_card = "Card 2 was chosen."
        expected_output_payment_card = 'Payment successful using card 2'
        expected_output_purchase = "Thank you for your purchase!"

        assert expected_output_login in captured.out.strip()
        assert expected_output_logout in captured.out.strip()
        assert expected_products in captured.out.strip()
        assert expected_items_added in captured.out.strip()
        assert expected_output_choose_card in captured.out.strip()
        assert expected_output_payment_card in captured.out.strip()
        assert expected_output_purchase in captured.out.strip()

    @pytest.mark.parametrize("user_inputs", [("Chirs", "Steve1", "n", "Steve", "Steve1", "all", "y", "70", "c", "y", "card", "2", "c", "y", "l")])
    # Unsuccessful Login --> User does not exists --> Not register --> Search products --> Ready to shop -->  Add Pen --> Check cart -->  Card --> Card 2 --> Check cart --> logout
    def test_6(self, capfd, user_inputs, copy_new_json_file):
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct('copy_users_new.json')

        with open("copy_users_new.json", 'r') as json_file:
            users_data = json.load(json_file)

        user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Steve"), None)

        assert users_data[user_index]["wallet"] == 85.0

        captured = capfd.readouterr()

        expected_output_login1 = "Username does not exists"
        expected_output_login2 = "Successfully logged in"
        expected_output_logout = "You have been logged out"
        expected_products = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
        expected_items_added = "Pens added to your cart."

        expected_output_empty_cart = "Your basket is empty. Please add items before checking out."
        expected_output_choose_card = "Card 2 was chosen."
        expected_output_payment_card = 'Payment successful using card 2'
        expected_output_purchase = "Thank you for your purchase!"

        assert expected_output_login1 in captured.out.strip()
        assert expected_output_login2 in captured.out.strip()
        assert expected_output_logout in captured.out.strip()
        assert expected_products in captured.out.strip()
        assert expected_items_added in captured.out.strip()
        assert expected_output_empty_cart in captured.out.strip()
        assert expected_output_choose_card in captured.out.strip()
        assert expected_output_payment_card in captured.out.strip()
        assert expected_output_purchase in captured.out.strip()

    @pytest.mark.parametrize("user_inputs", [("Steve", "asd", "Steve", "Steve1", "all", "y", "70", "c", "y", "card", "1", "c", "y", "l")])
    def test_7(self, capfd, user_inputs, copy_new_json_file):
    # Unsuccessful Login --> User does exists --> Search products --> Ready to shop -->  Add Pen --> Check cart -->  Card --> Card 1 --> Check cart --> logout
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct('copy_users_new.json')

        with open("copy_users_new.json", 'r') as json_file:
            users_data = json.load(json_file)

        user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Steve"), None)

        assert users_data[user_index]["wallet"] == 85.0

        captured = capfd.readouterr()

        expected_output_login1 = "Either username or password were incorrect"
        expected_output_login2 = "Successfully logged in"
        expected_output_logout = "You have been logged out"
        expected_products = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
        expected_items_added = "Pens added to your cart."

        expected_output_empty_cart = "Your basket is empty. Please add items before checking out."
        expected_output_choose_card = "Card 1 was chosen."
        expected_output_payment_card = 'Payment successful using card 1'
        expected_output_purchase = "Thank you for your purchase!"

        assert expected_output_login1 in captured.out.strip()
        assert expected_output_login2 in captured.out.strip()
        assert expected_output_logout in captured.out.strip()
        assert expected_products in captured.out.strip()
        assert expected_items_added in captured.out.strip()
        assert expected_output_empty_cart in captured.out.strip()
        assert expected_output_choose_card in captured.out.strip()
        assert expected_output_payment_card in captured.out.strip()
        assert expected_output_purchase in captured.out.strip()

    @pytest.mark.parametrize("user_inputs", [("Steve", "Steve1", "all", "y", "70", "l", "y")])
    def test_8(self, capfd, user_inputs, copy_new_json_file):
        # Successful Login --> User exists --> Search products --> Ready to shop -->  Add Pen --> logout
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct('copy_users_new.json')

        with open("copy_users_new.json", 'r') as json_file:
            users_data = json.load(json_file)

        user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Steve"), None)

        assert users_data[user_index]["wallet"] == 85.0

        captured = capfd.readouterr()

        expected_output_login = "Successfully logged in"
        expected_output_logout = "You have been logged out"
        expected_products = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
        expected_items_added = "Pens added to your cart."
        expected_output_logout_with_cart = "Your cart is not empty.You have following items\n['Pens', 0.5, 6]"

        assert expected_output_login in captured.out.strip()
        assert expected_output_logout in captured.out.strip()
        assert expected_products in captured.out.strip()
        assert expected_items_added in captured.out.strip()
        assert expected_output_logout_with_cart in captured.out.strip()

    @pytest.mark.parametrize("user_inputs", [("Steve", "Steve1", "all", "y", "55", "c", "y", "wallet", "l", "y")])
    def test_9(self, capfd, user_inputs, copy_new_json_file):
        # Successful Login --> User exists --> Search products --> Ready to shop -->  Add TV --> wallet --> Insufficient funds --> logout
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct('copy_users_new.json')

        with open("copy_users_new.json", 'r') as json_file:
            users_data = json.load(json_file)

        user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Steve"), None)

        assert users_data[user_index]["wallet"] == 85.0

        captured = capfd.readouterr()

        expected_output_login = "Successfully logged in"
        expected_output_logout = "You have been logged out"
        expected_products = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
        expected_items_added = "TV added to your cart."
        expected_insufficient_funds = "You don't have enough money to complete the purchase.\nPlease try again!"
        expected_output_logout_with_cart = "Your cart is not empty.You have following items\n['TV', 500.0, 1]"

        assert expected_output_login in captured.out.strip()
        assert expected_output_logout in captured.out.strip()
        assert expected_products in captured.out.strip()
        assert expected_items_added in captured.out.strip()
        assert expected_insufficient_funds in captured.out.strip()
        assert expected_output_logout_with_cart in captured.out.strip()

    @pytest.mark.parametrize("user_inputs", [("Steve", "Steve1", "all", "y", "55", "c", "y", "card", "1", "l")])
    def test_10(self, capfd, user_inputs, copy_new_json_file):
        # Successful Login --> User exists --> Search products --> Ready to shop -->  Add TV --> wallet --> Insufficient funds --> logout
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct('copy_users_new.json')

        with open("copy_users_new.json", 'r') as json_file:
            users_data = json.load(json_file)

        user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Steve"), None)

        assert users_data[user_index]["wallet"] == 85.0

        captured = capfd.readouterr()

        expected_output_login = "Successfully logged in"
        expected_output_logout = "You have been logged out"
        expected_products = "['Product', 'Price', 'Units']\n['Apple', '2', '10']"
        expected_items_added = "TV added to your cart."

        expected_output_choose_card = "Card 1 was chosen."
        expected_output_payment_card = 'Payment successful using card 1'
        expected_output_purchase = "Thank you for your purchase!"

        assert expected_output_login in captured.out.strip()
        assert expected_output_logout in captured.out.strip()
        assert expected_products in captured.out.strip()
        assert expected_items_added in captured.out.strip()

        assert expected_output_choose_card in captured.out.strip()
        assert expected_output_payment_card in captured.out.strip()
        assert expected_output_purchase in captured.out.strip()


