import csv, os, shutil, pytest, json, unittest, copy
from unittest import mock
from unittest.mock import patch
from checkout_and_payment import check_cart, checkout, User, Product, ShoppingCart, checkoutAndPayment, load_products_from_csv, choose_card
from logout import logout
from login import login
from products import display_csv_as_table, display_filtered_table, searchAndBuyProduct

@pytest.fixture()
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

            with open("copy_users_new.json", 'r') as json_file:
                users_data = json.load(json_file)

            user_index = next((index for index, u in enumerate(users_data) if u["username"] == "Steve"), None)

            assert users_data[user_index]["wallet"] == 100.0
            assert expected_output_login in captured.out.strip()
            assert expected_output_logout in captured.out.strip()

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
        expected_output_empty = "Your basket is empty. Please add items before checking out."

        assert expected_output_login in captured.out.strip()
        assert expected_output_logout in captured.out.strip()
        assert expected_output_empty in captured.out.strip()

    @pytest.mark.parametrize("user_inputs", [("Steve", "Steve1", "all", "Y", "71", "c", "y", "wrong", "wallet", "l")])
    def test_3(self, capfd, user_inputs, copy_new_json_file):
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
        expected_output_payment_method = "Invalid payment method. Please enter 'wallet' or 'card'."
        expected_output_purchase_wallet = "Thank you for your purchase, Steve! Your remaining balance is 85.0"

        assert expected_output_login in captured.out.strip()
        assert expected_output_logout in captured.out.strip()
        assert expected_output_payment_method in captured.out.strip()
        assert expected_output_purchase_wallet in captured.out.strip()

    def test_4(self):
        pass

    def test_5(self):
        pass

    def test_6(self):
        pass

    def test_7(self):
        pass

    def test_8(self):
        pass

    def test_9(self):
        pass

    def test_10(self):
        pass


