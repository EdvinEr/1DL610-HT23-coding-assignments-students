import csv, os, shutil, pytest, json, unittest, copy
from unittest import mock
from unittest.mock import patch
from checkout_and_payment import check_cart, checkout, User, Product, ShoppingCart, checkoutAndPayment, load_products_from_csv, choose_card
from logout import logout
from login import login
from products import display_csv_as_table, display_filtered_table, searchAndBuyProduct



class Test_smoke:
    #Successful Login User exist --> Search products --> Ready to shop --> logout
    @pytest.mark.parametrize("user_inputs", [("Steve", "Steve1", "all", "Y", "l")])
    def test_1(self, capfd, user_inputs):
            with patch('builtins.input', side_effect=user_inputs):
                searchAndBuyProduct()

            captured = capfd.readouterr()
            expected_output_login = "Successfully logged in"
            expected_output_logout = "You have been logged out"

            assert expected_output_login in captured.out.strip()
            assert expected_output_logout in captured.out.strip()

    @pytest.mark.parametrize("user_inputs", [("Steve", "Steve1", "all", "Y", "l")])
    def test_2(self):
        # Successful Login User exist --> Search products --> Ready to shop --> logout
        pass

    def test_3(self):
        pass

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


