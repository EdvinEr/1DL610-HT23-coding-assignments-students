import copy
import pytest
from unittest import mock
from logout import logout
from checkout_and_payment import ShoppingCart, Product


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


def test_logout_with_empty_cart(cart_empty):
    result = logout(cart=cart_empty)

    assert result == True
    assert len(cart_empty.items) == 0


@pytest.mark.parametrize("user_inputs", ["n", "No"])
def test_cancel_logout_cart_with_one_element(user_inputs, cart_with_one_element, capsys):
    copy_cart = copy.deepcopy(cart_with_one_element)

    with mock.patch('builtins.input', side_effect=user_inputs):
        result = logout(cart=cart_with_one_element)

    # Capture the printed output
    captured = capsys.readouterr()

    assert result == False
    assert len(cart_with_one_element.items) == len(copy_cart.items)
    assert create_expected_output(copy_cart) in captured.out


@pytest.mark.parametrize("user_inputs", ["n"])
def test_cancel_logout_cart_with_two_elements(user_inputs, cart_with_two_elements, capsys):
    copy_cart = copy.deepcopy(cart_with_two_elements)

    with mock.patch('builtins.input', side_effect=user_inputs):
        result = logout(cart=cart_with_two_elements)

    # Capture the printed output
    captured = capsys.readouterr()

    assert result == False
    assert len(cart_with_two_elements.items) == len(copy_cart.items)
    assert create_expected_output(copy_cart) in captured.out


@pytest.mark.parametrize("user_inputs", ["n"])
def test_cancel_logout_cart_with_multiple_elements(user_inputs, cart_with_multiple_elements, capsys):
    copy_cart = copy.deepcopy(cart_with_multiple_elements)

    with mock.patch('builtins.input', side_effect=user_inputs):
        result = logout(cart=cart_with_multiple_elements)

    # Capture the printed output
    captured = capsys.readouterr()

    assert result == False
    assert len(cart_with_multiple_elements.items) == len(copy_cart.items)
    assert create_expected_output(copy_cart) in captured.out


@pytest.mark.parametrize("user_inputs", ["y", "Yes"])
def test_logout_clear_cart_with_one_element(user_inputs, cart_with_one_element, capsys):
    copy_cart = copy.deepcopy(cart_with_one_element)

    with mock.patch('builtins.input', side_effect=user_inputs):
        result = logout(cart=cart_with_one_element)

    # Capture the printed output
    captured = capsys.readouterr()

    assert result == True
    assert len(cart_with_one_element.items) == 0
    assert create_expected_output(copy_cart) in captured.out


@pytest.mark.parametrize("user_inputs", ["y"])
def test_logout_clear_cart_with_two_elements(user_inputs, cart_with_two_elements, capsys):
    copy_cart = copy.deepcopy(cart_with_two_elements)

    with mock.patch('builtins.input', side_effect=user_inputs):
        result = logout(cart=cart_with_two_elements)

    # Capture the printed output
    captured = capsys.readouterr()

    assert result == True
    assert len(cart_with_two_elements.items) == 0
    assert create_expected_output(copy_cart) in captured.out


@pytest.mark.parametrize("user_inputs", ["y"])
def test_logout_clear_cart_with_multiple_elements(user_inputs, cart_with_multiple_elements, capsys):
    copy_cart = copy.deepcopy(cart_with_multiple_elements)

    with mock.patch('builtins.input', side_effect=user_inputs):
        result = logout(cart=cart_with_multiple_elements)

    # Capture the printed output
    captured = capsys.readouterr()

    assert result == True
    assert len(cart_with_multiple_elements.items) == 0
    assert create_expected_output(copy_cart) in captured.out

