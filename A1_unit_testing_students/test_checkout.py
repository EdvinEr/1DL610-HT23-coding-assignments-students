import csv
import os
import shutil

from checkout_and_payment import checkout, User, Product, ShoppingCart
import pytest

@pytest.fixture
def new_cart():
    return ShoppingCart()


def test_1_checkout(capfd, monkeypatch, new_cart):
    #Empty cart
    product_list = []
    user = User(name='Kim', wallet='20')
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    checkout(user, new_cart)

    captured = capfd.readouterr()

    assert captured.out.strip() == "Your basket is empty. Please add items before checking out."
    assert user.wallet == 20
    assert len(new_cart.retrieve_item()) == 0
    assert len(product_list) == 0


def test_2_checkout(capfd, monkeypatch, new_cart):
    # Not enough money
    product_list = [Product(name='Orange', price=200, units=1)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name='Kim', wallet=100)
    new_cart.add_item(product_list[0])
    checkout(user, new_cart)

    captured = capfd.readouterr()
    assert captured.out.strip() == f"You don't have enough money to complete the purchase.\nPlease try again!"
    assert user.wallet == 100
    assert len(new_cart.retrieve_item()) == 1
    assert len(product_list) == 1


def test_3_checkout(capfd, monkeypatch, new_cart):
    #Successful checkout
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

def test_4_checkout(capfd, monkeypatch, new_cart):
    #Multiple items in cart
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

def test_5_checkout(monkeypatch, new_cart):
    #Not enough available units than wanted
    product_list = [Product(name='Orange', price=10, units=1)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name='Kim', wallet=100)

    new_cart.add_item(product_list[0])
    new_cart.add_item(product_list[0])

    checkout(user, new_cart)

    assert user.wallet == 80
    assert len(new_cart.retrieve_item()) == 0
    assert len(product_list) == 0


def test_6_checkout(capfd, monkeypatch, new_cart):
    #Negative wallet
    product_list = [Product(name='Orange', price=10, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name='Kim', wallet=-100)

    new_cart.add_item(product_list[0])

    checkout(user, new_cart)

    captured = capfd.readouterr()
    expected_output = f"You don't have enough money to complete the purchase.\nPlease try again!"
    assert captured.out.strip() == expected_output

    assert user.wallet == -100
    assert len(new_cart.retrieve_item()) == 1
    assert product_list[0].units == 3


def test_7_checkout(capfd, monkeypatch, new_cart):
    #Product with negative price
    product_list = [Product(name='Orange', price=-10, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name='Kim', wallet=100)

    new_cart.add_item(product_list[0])

    checkout(user, new_cart)

    captured = capfd.readouterr()

    expected_output = f"Thank you for your purchase, {user.name}! Your remaining balance is {user.wallet}"
    assert captured.out.strip() == expected_output

    #Note that this means that the user gets 20.
    assert user.wallet == 110
    assert len(new_cart.retrieve_item()) == 0
    assert product_list[0].units == 2

def test_8_checkout(monkeypatch, new_cart):
    #Checkout when a product only has one unit left
    product_list = [Product(name='Orange', price=10, units=1)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name='Kim', wallet=100)
    new_cart.add_item(product_list[0])

    checkout(user, new_cart)

    assert user.wallet == 90
    assert len(product_list) == 0

def test_9_checkout(monkeypatch, new_cart):
    #User with wallet with decimal balance
    product_list = [Product(name='Orange', price=10, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name='Kim', wallet=100.5)
    new_cart.add_item(product_list[0])

    checkout(user, new_cart)

    assert user.wallet == 90.5
    assert len(new_cart.retrieve_item()) == 0
    assert product_list[0].units == 2

def test_10_checkout(monkeypatch, new_cart):
    #Not enough available units (0)
    product_list = [Product(name='Orange', price=10, units=0)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name='Kim', wallet=100)

    new_cart.add_item(product_list[0])

    checkout(user, new_cart)

    assert user.wallet == 90
    assert len(new_cart.retrieve_item()) == 0
    assert product_list[0].units == -1
