import csv
import os
import shutil
import unittest.mock

from checkout_and_payment import check_cart, checkout, User, Product, ShoppingCart
import pytest

@pytest.fixture
def checkout_stub1(mocker):
    return mocker.patch('checkout_and_payment.checkout', return_value='None')

def test_1_check_cart():
    #Check cart with no checkout
    user = User(name="Charlie", wallet='500')
    cart = ShoppingCart()
    product = Product(name='TV', price=300, units=3)
    cart.add_item(product)

    with unittest.mock.patch('builtins.input', return_value='n'):
        result = check_cart(user, cart)

    assert result == False

def test_2_check_cart(checkout_stub1, monkeypatch):
    user = User(name="Lisa", wallet='700')
    cart = ShoppingCart()
    product = Product(name='Mobile', price=200, units=3)
    cart.add_item(product)

    monkeypatch.setattr('builtins.input', lambda _: 'y')

    result = check_cart(user, cart)

    assert result != False
    checkout_stub1.assert_called_once_with(user, cart)

