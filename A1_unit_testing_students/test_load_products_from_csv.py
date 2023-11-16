import csv
import os
import shutil

from checkout_and_payment import load_products_from_csv
import pytest


@pytest.fixture(scope='module')
def copy_csv_file():
    shutil.copy('products.csv', 'copy_products.csv')
    products = load_products_from_csv('copy_products.csv')
    yield products
    os.remove('copy_products.csv')


def test_first_load_products_from_csv(copy_csv_file):
    products = copy_csv_file
    assert products[0].name == 'Apple'
    assert products[0].price == 2.0
    assert products[0].units == 10


def test_sec_load_products_from_csv(copy_csv_file):
    products = copy_csv_file
    assert products[1].name == 'Banana'
    assert products[1].price == 1.0
    assert products[1].units == 15
