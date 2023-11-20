import csv
import os
import shutil

from checkout_and_payment import checkout, User, Product, ShoppingCart
import pytest


def test_1_checkout(capfd):
    #Empty cart
    user = User(name='Chris', wallet='20')
    cart = ShoppingCart()

    checkout(user, cart)

    captured = capfd.readouterr()

    assert captured.out.strip() == "Your basket is empty. Please add items before checking out."
    assert user.wallet == 20
    assert len(cart.retrieve_item()) == 0


def test_2_checkout():
    # Not enough money
    user = User(name='Fred', wallet=20)
    cart = ShoppingCart()
    product = Product(name='Apple', price=50, units=3)
    cart.add_item(product)
    checkout(user, cart)
    assert user.wallet == 20
    assert len(cart.retrieve_item()) == 1


def test_3_checkout(capfd):
    #Successful checkout
    #Check that cart is empty afterwards
    user = User(name='Alice', wallet=200)
    cart = ShoppingCart()
    product = Product(name='Orange', price=20, units=3)
    cart.add_item(product)

    checkout(user, cart)

    captured = capfd.readouterr()

    expected_output = f"Thank you for your purchase, {user.name}! Your remaining balance is {user.wallet}"
    assert captured.out.strip() == expected_output
    assert user.wallet == 180
    assert len(cart.retrieve_item()) == 0
    assert product.units == 2

def test_4_checkout(capfd):
    #Multiple items in cart
    user = User(name='Erwin', wallet=500)
    cart = ShoppingCart()
    product1 = Product(name='Fries', price=100, units=3)
    product2 = Product(name='Burger', price=30, units=2)
    cart = ShoppingCart()
    cart.add_item(product1)
    cart.add_item(product2)

    checkout(user, cart)

    captured = capfd.readouterr()
    expected_output = f"Thank you for your purchase, {user.name}! Your remaining balance is {user.wallet}"
    assert captured.out.strip() == expected_output
    assert user.wallet == 370
    assert len(cart.retrieve_item()) == 0
    assert product1.units == 2
    assert product2.units == 1

#def test_5_checkout():
    #Not enough available units
   # assert False

#def test_6_checkout():
    #Negative wallet
    #assert False

#def test_7_checkout():
    #Product with negative price
    #assert False

#def test_8_checkout():
    #Are the products removed/units after checkout?
    #assert False

#def test_9_checkout():
    #What if the cart contains products that does not exist?
    #assert False

#def test_10_checkout():
    #
    #assert False