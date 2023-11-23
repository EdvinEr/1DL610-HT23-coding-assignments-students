import csv
import os
import shutil
import unittest.mock

from checkout_and_payment import check_cart, checkout, User, Product, ShoppingCart
import pytest

@pytest.fixture
def checkout_stub1(mocker):
    return mocker.patch('checkout_and_payment.checkout', return_value=None)

@pytest.fixture
def new_cart():
    return ShoppingCart()

#Test with product in cart, but no checkout
def test_EC1(monkeypatch, new_cart, checkout_stub1):
    product_list = [Product(name='Orange', price=10, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Kim", wallet='100')

    new_cart.add_item(product_list[0])

    with unittest.mock.patch('builtins.input', return_value='n'):
        result = check_cart(user, new_cart)
    assert result == False
    checkout_stub1.assert_not_called()

#Test with product in cart, checkout
def test_EC2(checkout_stub1, new_cart, monkeypatch):
    product_list = [Product(name='Orange', price=10, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Kim", wallet='100')

    new_cart.add_item(product_list[0])

    monkeypatch.setattr('builtins.input', lambda _: 'y')

    result = check_cart(user, new_cart)

    assert result == None
    checkout_stub1.assert_called_once_with(user, new_cart)

#Test with multiple products in cart, checkout
def test_EC3(checkout_stub1, new_cart, monkeypatch):
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
def test_EC4(checkout_stub1, new_cart, monkeypatch):
    user = User(name="Kim", wallet='100')
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    result = check_cart(user, new_cart)

    assert result == None
    checkout_stub1.assert_called_once_with(user, new_cart)

#Test with multiple products in cart, but no checkout
def test_EC5(checkout_stub1, new_cart, monkeypatch):
    product_list = [Product(name='Orange', price=10, units=3), Product(name='Apple', price='2', units='10')]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Kim", wallet='100')

    new_cart.add_item(product_list[0])
    new_cart.add_item(product_list[1])

    monkeypatch.setattr('builtins.input', lambda _: 'n')
    result = check_cart(user, new_cart)

    assert result == False
    checkout_stub1.assert_not_called()

#Test to check cart with wrong input
def test_EC6(checkout_stub1, new_cart, monkeypatch):
    product_list = [Product(name='Orange', price=10, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Kim", wallet='100')

    new_cart.add_item(product_list[0])

    monkeypatch.setattr('builtins.input', lambda _: 't')
    result = check_cart(user, new_cart)

    assert result == False
    checkout_stub1.assert_not_called()

#Test with an empty cart, no checkout
def test_EC7(checkout_stub1, new_cart, monkeypatch):
    user = User(name="Kim", wallet='100')
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    result = check_cart(user, new_cart)

    assert result == False
    checkout_stub1.assert_not_called()

#Test with insufficient wallet funds, no checkout
def test_EC8(checkout_stub1, new_cart, monkeypatch):
    product_list = [Product(name='Orange', price=10, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Kim", wallet='0')

    new_cart.add_item(product_list[0])

    monkeypatch.setattr('builtins.input', lambda _: 'n')
    result = check_cart(user, new_cart)

    assert result == False
    checkout_stub1.assert_not_called()

#Test with negative product price
def test_EC9(checkout_stub1, new_cart, monkeypatch):
    # Negative price products
    product_list = [Product(name='Orange', price=-10, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Kim", wallet='100')

    new_cart.add_item(product_list[0])

    monkeypatch.setattr('builtins.input', lambda _: 'y')
    result = check_cart(user, new_cart)

    assert result == None
    checkout_stub1.assert_called_once_with(user, new_cart)

#Test with negative product units
def test_EC10(checkout_stub1, new_cart, monkeypatch):
    # Negative units
    product_list = [Product(name='Orange', price=10, units=-1)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Kim", wallet='100')

    new_cart.add_item(product_list[0])

    monkeypatch.setattr('builtins.input', lambda _: 'y')
    result = check_cart(user, new_cart)

    assert result == None
    checkout_stub1.assert_called_once_with(user, new_cart)