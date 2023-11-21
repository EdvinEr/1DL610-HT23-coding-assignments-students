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

def test_1_check_cart(monkeypatch, new_cart, checkout_stub1):
    # Check cart with product in cart, but no checkout
    product_list = [Product(name='TV', price=300, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Charlie", wallet='500')

    new_cart.add_item(product_list[0])

    with unittest.mock.patch('builtins.input', return_value='n'):
        result = check_cart(user, new_cart)
    assert result == False
    checkout_stub1.assert_not_called()


def test_2_check_cart(checkout_stub1, new_cart, monkeypatch):
    # Check cart with product in cart, checkout
    product_list = [Product(name='Mobile', price=200, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Lisa", wallet='700')

    new_cart.add_item(product_list[0])

    monkeypatch.setattr('builtins.input', lambda _: 'y')

    result = check_cart(user, new_cart)

    assert result == None
    checkout_stub1.assert_called_once_with(user, new_cart)

def test_3_check_cart(checkout_stub1, new_cart, monkeypatch):
    # Check cart with multiple products in cart, checkout
    product_list = [Product(name='Car', price=300, units=3), Product(name='Apple', price='2', units='10')]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Lando", wallet='500')

    new_cart.add_item(product_list[0])
    new_cart.add_item(product_list[1])

    monkeypatch.setattr('builtins.input', lambda _: 'y')
    result = check_cart(user, new_cart)

    assert result == None
    checkout_stub1.assert_called_once_with(user, new_cart)


def test_4_check_cart(checkout_stub1, new_cart, monkeypatch):
    # Check cart with empty cart, checkout
    user = User(name="Chris", wallet='100')
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    result = check_cart(user, new_cart)

    assert result == None
    checkout_stub1.assert_called_once_with(user, new_cart)


def test_5_check_cart(checkout_stub1, new_cart, monkeypatch):
    # Check cart with multiple products in cart, no checkout
    product_list = [Product(name='Rose', price=300, units=3), Product(name='Apple', price='2', units='10')]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Tom", wallet='500')

    new_cart.add_item(product_list[0])
    new_cart.add_item(product_list[1])

    monkeypatch.setattr('builtins.input', lambda _: 'n')
    result = check_cart(user, new_cart)

    assert result == False
    checkout_stub1.assert_not_called()


def test_6_check_cart(checkout_stub1, new_cart, monkeypatch):
    # Check cart wrong input
    product_list = [Product(name='Rose', price=300, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Tom", wallet='500')

    new_cart.add_item(product_list[0])

    monkeypatch.setattr('builtins.input', lambda _: 't')
    result = check_cart(user, new_cart)

    assert result == False
    checkout_stub1.assert_not_called()


def test_7_check_cart(checkout_stub1, new_cart, monkeypatch):
    # Check empty cart, no checkout
    user = User(name="Chris", wallet='100')
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    result = check_cart(user, new_cart)

    assert result == False
    checkout_stub1.assert_not_called()

def test_8_check_cart(checkout_stub1, new_cart, monkeypatch):
    # User with no money in wallet, no checkout
    product_list = [Product(name='Rose', price=300, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Tom", wallet='0')

    new_cart.add_item(product_list[0])

    monkeypatch.setattr('builtins.input', lambda _: 'n')
    result = check_cart(user, new_cart)

    assert result == False
    checkout_stub1.assert_not_called()

def test_9_check_cart(checkout_stub1, new_cart, monkeypatch):
    # Negative price products
    product_list = [Product(name='Rose', price=-300, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Tom", wallet='400')

    new_cart.add_item(product_list[0])

    monkeypatch.setattr('builtins.input', lambda _: 'y')
    result = check_cart(user, new_cart)

    assert result == None
    checkout_stub1.assert_called_once_with(user, new_cart)


def test_10_check_cart(checkout_stub1, new_cart, monkeypatch):
    # Negative units
    product_list = [Product(name='Rose', price=-300, units=-1)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name="Tom", wallet='400')

    new_cart.add_item(product_list[0])

    monkeypatch.setattr('builtins.input', lambda _: 'y')
    result = check_cart(user, new_cart)

    assert result == None
    checkout_stub1.assert_called_once_with(user, new_cart)