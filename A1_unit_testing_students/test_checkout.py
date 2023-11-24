import csv
import os
import shutil

from checkout_and_payment import checkout, User, Product, ShoppingCart
import pytest

@pytest.fixture
def new_cart():
    return ShoppingCart()

#Test with an empty cart
def test_EC1(capfd, monkeypatch, new_cart):
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
def test_EC2(capfd, monkeypatch, new_cart):
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
def test_EC3(capfd, monkeypatch, new_cart):
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
def test_EC4(capfd, monkeypatch, new_cart):
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
def test_EC5(monkeypatch, new_cart):
    product_list = [Product(name='Orange', price=10, units=1)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name='Kim', wallet=100)

    new_cart.add_item(product_list[0])
    new_cart.add_item(product_list[0])

    checkout(user, new_cart)

    assert user.wallet == 80
    assert len(new_cart.retrieve_item()) == 0
    assert len(product_list) == 0

#Test with negative wallet
def test_EC6(capfd, monkeypatch, new_cart):
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

#Test with products having negative price
def test_EC7(capfd, monkeypatch, new_cart):
    product_list = [Product(name='Orange', price=-10, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name='Kim', wallet=100)

    new_cart.add_item(product_list[0])

    checkout(user, new_cart)

    captured = capfd.readouterr()

    expected_output = f"Thank you for your purchase, {user.name}! Your remaining balance is {user.wallet}"
    assert captured.out.strip() == expected_output

    assert user.wallet == 110
    assert len(new_cart.retrieve_item()) == 0
    assert product_list[0].units == 2

#Test when only one unit left
def test_EC8(monkeypatch, new_cart):
    product_list = [Product(name='Orange', price=10, units=1)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name='Kim', wallet=100)
    new_cart.add_item(product_list[0])

    checkout(user, new_cart)

    assert user.wallet == 90
    assert len(product_list) == 0

#Test with wallet having decimal balance
def test_EC9(monkeypatch, new_cart):
    product_list = [Product(name='Orange', price=10, units=3)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name='Kim', wallet=100.5)
    new_cart.add_item(product_list[0])

    checkout(user, new_cart)

    assert user.wallet == 90.5
    assert len(new_cart.retrieve_item()) == 0
    assert product_list[0].units == 2

#Test with not enough available units from the start
def test_EC10(monkeypatch, new_cart):
    product_list = [Product(name='Orange', price=10, units=0)]
    monkeypatch.setattr('checkout_and_payment.products', product_list)
    user = User(name='Kim', wallet=100)

    new_cart.add_item(product_list[0])

    checkout(user, new_cart)

    assert user.wallet == 90
    assert len(new_cart.retrieve_item()) == 0
    assert product_list[0].units == -1
