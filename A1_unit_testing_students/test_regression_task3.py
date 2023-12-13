import csv, os, shutil, pytest, json, unittest, copy
from unittest import mock
from unittest.mock import patch
from checkout_and_payment import check_cart, checkout, User, Product, ShoppingCart, checkoutAndPayment, load_products_from_csv
from logout import logout
from login import login
from products import display_csv_as_table, display_filtered_table, searchAndBuyProduct

@pytest.fixture
def json_dump_mock(monkeypatch):
    # Create a MagicMock for json.dump
    mock_dump = mock.MagicMock()
    monkeypatch.setattr('json.dump', mock_dump)
    return mock_dump

@pytest.fixture
def registered_user1():
    return {"username": "testuser", "password": "Test_Password", "wallet": 0}

@pytest.fixture
def registered_user2():
    return {"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100}

@pytest.fixture
def login_open_users_file_stub(monkeypatch, registered_user1):
    # Provide user file content for the login function
    read_data = json.dumps([registered_user1])
    monkeypatch.setattr('builtins.open', mock.mock_open(read_data=read_data))

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

def create_expected_output(cart):
    expected_output = "Your cart is not empty.You have following items\n"
    for i in cart.retrieve_item():
        product = i.get_product()
        expected_output += f"['{product[0]}', {product[1]}, {product[2]}]\n"
    return expected_output

@pytest.fixture
def cart_empty():
    return ShoppingCart()

@pytest.fixture
def cart_with_one_element():
    cart = ShoppingCart()
    cart.add_item(Product(name="Apple", price=5, units=10))
    return cart

@pytest.fixture
def cart_with_two_elements():
    cart = ShoppingCart()
    cart.add_item(Product(name="Apple", price=5, units=10))
    cart.add_item(Product(name="Banana", price=10, units=2))
    return cart

@pytest.fixture
def cart_with_multiple_elements():
    cart = ShoppingCart()
    cart.add_item(Product(name="Apple", price=5, units=10))
    cart.add_item(Product(name="Banana", price=10, units=2))
    cart.add_item(Product(name="Orange", price=12, units=5))
    return cart

@pytest.fixture(scope='module')
def empty_csv_file():
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
def modify_csv_file():
    shutil.copy('products.csv', 'modify_products.csv')
    yield 'modify_products.csv'
    os.remove('modify_products.csv')

@pytest.fixture(scope='module')
def copy_csv_file():
    shutil.copy('products.csv', 'copy_products.csv')
    products = load_products_from_csv('copy_products.csv')
    print("----------setup----------")
    yield products
    os.remove('copy_products.csv')
    print("----------teardown----------")

@pytest.fixture
def checkout_stub1(mocker):
    return mocker.patch('checkout_and_payment.checkout', return_value=None)

@pytest.fixture
def new_cart():
    return ShoppingCart()

@pytest.fixture
def open_users_file_stub(monkeypatch, registered_user2):
    # Provide user file content for the login function
    read_data = json.dumps([registered_user2])
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

@pytest.fixture
def new_cart():
    return ShoppingCart()


class TestSuiteCheckCart:
    #Test with product in cart, but no checkout
    def test_EC1(self, monkeypatch, new_cart, checkout_stub1):
        product_list = [Product(name='Orange', price=10, units=3)]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name="Kim", wallet='100')

        new_cart.add_item(product_list[0])

        with unittest.mock.patch('builtins.input', return_value='n'):
            result = check_cart(user, new_cart)
        assert result == False
        checkout_stub1.assert_not_called()

    #Test with product in cart, checkout
    def test_EC2(self, checkout_stub1, new_cart, monkeypatch):
        product_list = [Product(name='Orange', price=10, units=3)]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name="Kim", wallet='100')

        new_cart.add_item(product_list[0])

        monkeypatch.setattr('builtins.input', lambda _: 'y')

        result = check_cart(user, new_cart)

        assert result == None
        checkout_stub1.assert_called_once_with(user, new_cart)

    #Test with multiple products in cart, checkout
    def test_EC3(self, checkout_stub1, new_cart, monkeypatch):
        product_list = [Product(name='Orange', price=10, units=3), Product(name='Apple', price='2', units='10')]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name="Kim", wallet='100')

        new_cart.add_item(product_list[0])
        new_cart.add_item(product_list[1])

        monkeypatch.setattr('builtins.input', lambda _: 'y')
        result = check_cart(user, new_cart)

        assert result == None
        checkout_stub1.assert_called_once_with(user, new_cart)

    #Test with empty cart, checkout
    def test_EC4(self, checkout_stub1, new_cart, monkeypatch):
        user = User(name="Kim", wallet='100')
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        result = check_cart(user, new_cart)

        assert result == None
        checkout_stub1.assert_called_once_with(user, new_cart)

    #Test with multiple products in cart, but no checkout
    def test_EC5(self, checkout_stub1, new_cart, monkeypatch):
        product_list = [Product(name='Orange', price=10, units=3), Product(name='Apple', price='2', units='10')]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name="Kim", wallet='100')

        new_cart.add_item(product_list[0])
        new_cart.add_item(product_list[1])

        monkeypatch.setattr('builtins.input', lambda _: 'n')
        result = check_cart(user, new_cart)

        assert result == False
        checkout_stub1.assert_not_called()

class TestSuiteCheckoutAndPayment:
    def test_printout_logout_confirmed(self, logout_stub1, capsys, monkeypatch):
        login_info = {"username": "Ramanathan", "wallet": 100}
        monkeypatch.setattr("checkout_and_payment.products", [])
        monkeypatch.setattr("builtins.input", mimic_input(["l"]))
        checkoutAndPayment(login_info)
        out, err = capsys.readouterr()
        expected_output = "You have been logged out"
        assert expected_output in out[:28]

    def test_printout_one_product(self, logout_stub1, capsys, monkeypatch):
        login_info = {"username": "Ramanathan", "wallet": 100}
        products = [Product("Ice cream", 10, 2)]
        monkeypatch.setattr("checkout_and_payment.products", products)
        monkeypatch.setattr("builtins.input", mimic_input(["l"]))
        checkoutAndPayment(login_info)
        out, err = capsys.readouterr()
        expected_o = "1. Ice cream - $10.0 - Units: 2"
        assert expected_o in out[:31]
    
    def test_printout_multiple_products(self, logout_stub1, capsys, monkeypatch):
        login_info = {"username": "Ramanathan", "wallet": 100}
        products = [Product("Ice cream", 10, 2), Product("Chocolate", 15, 5), Product("Popcorns", 8, 3)]
        monkeypatch.setattr("checkout_and_payment.products", products)
        monkeypatch.setattr("builtins.input", mimic_input(["l"]))
        checkoutAndPayment(login_info)
        out, err = capsys.readouterr()
        expected_o = "1. Ice cream - $10.0 - Units: 2\n2. Chocolate - $15.0 - Units: 5\n3. Popcorns - $8.0 - Units: 3"
        assert expected_o in out[:96]
    
    def test_printout_add_item_to_cart(self, logout_stub1, capsys, monkeypatch):
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
    
    def test_printout_item_out_of_stock(self, logout_stub1, capsys, monkeypatch):
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

class TestSuiteCheckout:
    #Test with an empty cart
    def test_EC1(self, capfd, monkeypatch, new_cart):
        product_list = []
        user = User(name='Kim', wallet='20')
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        checkout(user, new_cart)

        captured = capfd.readouterr()

        assert captured.out.strip() == "Your basket is empty. Please add items before checking out."
        assert user.wallet == 20
        assert len(new_cart.retrieve_item()) == 0
        assert len(product_list) == 0

    #Test with not enough money
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

    #Test a valid checkout
    def test_EC3(self, capfd, monkeypatch, new_cart):
        product_list = [Product(name='Orange', price=10, units=3)]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name='Kim', wallet=100)
        new_cart.add_item(product_list[0])

        checkout(user, new_cart)

        captured = capfd.readouterr()

        expected_output = f"Thank you for your purchase, {user.name}! Your remaining balance is {user.wallet}"
        assert captured.out.strip() == expected_output
        assert user.wallet == 90
        assert len(new_cart.retrieve_item()) == 0
        assert product_list[0].units == 2

    #Test with multiple items in cart
    def test_EC4(self, capfd, monkeypatch, new_cart):
        product_list = [Product(name='Orange', price=10, units=3), Product(name='Apple', price=20, units=2)]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name='Kim', wallet=100)

        new_cart.add_item(product_list[0])
        new_cart.add_item(product_list[1])

        checkout(user, new_cart)

        captured = capfd.readouterr()
        expected_output = f"Thank you for your purchase, {user.name}! Your remaining balance is {user.wallet}"
        assert captured.out.strip() == expected_output
        assert user.wallet == 70
        assert len(new_cart.retrieve_item()) == 0
        assert product_list[0].units == 2
        assert product_list[1].units == 1

    #Test with not enough available units than wanted
    def test_EC5(self, monkeypatch, new_cart):
        product_list = [Product(name='Orange', price=10, units=1)]
        monkeypatch.setattr('checkout_and_payment.products', product_list)
        user = User(name='Kim', wallet=100)

        new_cart.add_item(product_list[0])
        new_cart.add_item(product_list[0])

        checkout(user, new_cart)

        assert user.wallet == 80
        assert len(new_cart.retrieve_item()) == 0
        assert len(product_list) == 0


class TestSuiteDisplayCSVAsTable:
    # Test a non-existing file
    def test_EC1(self):
        with pytest.raises(FileNotFoundError):
            display_csv_as_table("non_existing_file.csv")

    # Test an empty csv file
    def test_EC2(self, capsys):
        display_csv_as_table("test_files/test_empty.csv")
        out, err = capsys.readouterr()
        assert out == ""

    # Test an empty string as input
    def test_EC3(self):
        with pytest.raises(FileNotFoundError):
            display_csv_as_table("")

    # Test a csv file with only 1 column
    def test_EC4(self, capsys):
        display_csv_as_table("test_files/test_1_column.csv")
        out, err = capsys.readouterr()
        assert out == "['Product']\n['0']\n['1']\n['2']\n['3']\n['4']\n"

    # Test a csv file containing an empty row
    def test_EC5(self, capsys):
        display_csv_as_table("test_files/test_empty_row.csv")
        out, err = capsys.readouterr()
        assert out[73:75] == "[]"

class TestSuiteDisplayFilteredTable:
    # Test a non-existing file
    def test_EC1(self):
        with pytest.raises(FileNotFoundError):
            display_filtered_table("non_existing_file.csv", "Apple")

    # Test an empty csv file
    def test_EC2(self, capsys):
        display_filtered_table("test_files/test_empty.csv", "Apple")
        out, err = capsys.readouterr()
        assert out == ""

    # Test an empty string as csv file input
    def test_EC3(self):
        with pytest.raises(FileNotFoundError):
            display_filtered_table("", "Apple")

    # Test an empty string as search input
    def test_EC4(self, capsys, copy_csv_file):
        display_filtered_table("copy_products.csv", "")
        out, err = capsys.readouterr()
        assert out == "['Product', 'Price', 'Units']\n"

    # Test a csv file with only 1 column
    def test_EC5(self, capsys):
        display_filtered_table("test_files/test_1_column.csv", "1")
        out, err = capsys.readouterr()
        assert out == "['Product']\n['1']\n"

class TestSuiteLoadProductsFromCSV:
    #Test a non-existing file
    def test_EC1(self):
        with pytest.raises(FileNotFoundError):
            assert load_products_from_csv("non_existing.csv")

    #Test an empty csv file
    def test_EC2(self, empty_csv_file):
        empty_products = empty_csv_file
        assert len(empty_products) == 0
        assert empty_products == []

    #Test an empty string as input
    def test_EC3(self):
        with pytest.raises(FileNotFoundError):
            load_products_from_csv("")

    #Test correct output
    def test_EC4(self, copy_csv_file):
        products = copy_csv_file
        assert products[0].name == 'Apple'
        assert products[0].price == 2.0
        assert products[0].units == 10

        assert products[1].name == 'Banana'
        assert products[1].price == 1.0
        assert products[1].units == 15

        expected_length = 71
        assert len(products) == expected_length

    #Test when products have negative or no price
    def test_EC5(self, modify_csv_file):
        with open(modify_csv_file, mode='a', newline='') as csvfile:
            fields = ['Product', 'Price', 'Units']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            csvfile.write('\n')
            writer.writerow({'Product': 'Bread', 'Price': '-3.0', 'Units': '20'})
            writer.writerow({'Product': 'Ham', 'Price': '0', 'Units': '10'})

        modified_products = load_products_from_csv(modify_csv_file)

        assert modified_products[71].price == -3.0
        assert modified_products[72].price == 0

class TestSuiteLogin:
    @pytest.mark.parametrize("user_inputs", [("testuser", "Test_Password")])
    def test_login_successful(self, user_inputs, login_open_users_file_stub, json_dump_mock, capsys):
        # Run the login function
        with mock.patch('builtins.input', side_effect=user_inputs):
            login()

        # Capture the printed output
        captured = capsys.readouterr()

        # Assert the output contains the expected message
        assert "Successfully logged in" in captured.out

        json_dump_mock.assert_not_called()


    @pytest.mark.parametrize("user_inputs", [
        ("testuser", "wrongpassword")
    ])
    def test_login_with_incorrect_password(self, user_inputs, login_open_users_file_stub, json_dump_mock, capsys):
        # Run the login function
        with mock.patch('builtins.input', side_effect=user_inputs):
            login()

        # Capture the printed output
        captured = capsys.readouterr()

        # Assert the output contains the expected message
        assert "Either username or password were incorrect" in captured.out

        json_dump_mock.assert_not_called()


    @pytest.mark.parametrize("user_inputs", [
        ("non_existing_user", "wrongpassword", "N"),
        ("non_existing_user", "Test_Password", "N")
    ])
    def test_login_with_non_existing_username_and_not_register(self, user_inputs, login_open_users_file_stub, json_dump_mock, capsys):
        # Run the login function
        with mock.patch('builtins.input', side_effect=user_inputs):
            login()

        # Capture the printed output
        captured = capsys.readouterr()

        # Assert the output contains the expected message
        assert "Username does not exists." in captured.out

        json_dump_mock.assert_not_called()


    @pytest.mark.parametrize("user_inputs", [
        ("non_existing_user", "password", "Y", "Correct_New_Password")
    ])
    def test_login_failed_and_register_correct(self, user_inputs, login_open_users_file_stub, json_dump_mock, capsys):
        # Run the login function
        with mock.patch('builtins.input', side_effect=user_inputs):
            login()

        # Capture the printed output
        captured = capsys.readouterr()

        # Assert the output contains the expected message
        assert "Username does not exists." in captured.out
        assert "Successfully registered" in captured.out

        json_dump_mock.assert_called_once()

class TestSuiteLogout:
    def test_logout_with_empty_cart(self, cart_empty):
        result = logout(cart=cart_empty)
    
        assert result == True
        assert len(cart_empty.items) == 0
    
    
    @pytest.mark.parametrize("user_inputs", ["n", "No"])
    def test_cancel_logout_cart_with_one_element(self, user_inputs, cart_with_one_element, capsys):
        copy_cart = copy.deepcopy(cart_with_one_element)
    
        with mock.patch('builtins.input', side_effect=user_inputs):
            result = logout(cart=cart_with_one_element)
    
        # Capture the printed output
        captured = capsys.readouterr()
    
        assert result == False
        assert len(cart_with_one_element.items) == len(copy_cart.items)
        assert create_expected_output(copy_cart) in captured.out
    
    
    @pytest.mark.parametrize("user_inputs", ["n"])
    def test_cancel_logout_cart_with_two_elements(self, user_inputs, cart_with_two_elements, capsys):
        copy_cart = copy.deepcopy(cart_with_two_elements)
    
        with mock.patch('builtins.input', side_effect=user_inputs):
            result = logout(cart=cart_with_two_elements)
    
        # Capture the printed output
        captured = capsys.readouterr()
    
        assert result == False
        assert len(cart_with_two_elements.items) == len(copy_cart.items)
        assert create_expected_output(copy_cart) in captured.out
    
    
    @pytest.mark.parametrize("user_inputs", ["n"])
    def test_cancel_logout_cart_with_multiple_elements(self, user_inputs, cart_with_multiple_elements, capsys):
        copy_cart = copy.deepcopy(cart_with_multiple_elements)
    
        with mock.patch('builtins.input', side_effect=user_inputs):
            result = logout(cart=cart_with_multiple_elements)
    
        # Capture the printed output
        captured = capsys.readouterr()
    
        assert result == False
        assert len(cart_with_multiple_elements.items) == len(copy_cart.items)
        assert create_expected_output(copy_cart) in captured.out

class TestSuiteSearchAndBuyProduct:
    @pytest.mark.parametrize("user_inputs", [("all", "Y")])
    def test_with_stubs1(self, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct()

        login_stub.assert_called_once()
        display_csv_as_table_stub.assert_called_once()
        display_filtered_table_stub.assert_not_called()
        checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100 })

    @pytest.mark.parametrize("user_inputs", [("Apple", "Y")])
    def test_with_stubs2(self, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct()

        login_stub.assert_called_once()
        display_csv_as_table_stub.assert_not_called()
        display_filtered_table_stub.assert_called_once()
        checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100 })

    @pytest.mark.parametrize("user_inputs", [("Apple", "N", "all", "Y")])
    def test_with_stubs3(self, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
        with patch('builtins.input', side_effect=user_inputs):
            searchAndBuyProduct()

        login_stub.assert_called_once()
        display_csv_as_table_stub.assert_called_once()
        display_filtered_table_stub.assert_called_once()
        checkoutAndPayment_stub.assert_called_once_with({"username": "Ramanathan", "wallet": 100})

    def test_with_stubs4(self, login_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub):
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
    def test_with_stubs5(self, login_fail_stub, checkoutAndPayment_stub, display_csv_as_table_stub, display_filtered_table_stub, user_inputs):
        with patch('builtins.input', side_effect=user_inputs):
            with pytest.raises(Exception, match="Login failed"):
                searchAndBuyProduct()

        assert login_fail_stub.call_count >= 2
        display_csv_as_table_stub.assert_not_called()
        display_filtered_table_stub.assert_not_called()
        checkoutAndPayment_stub.assert_not_called()
