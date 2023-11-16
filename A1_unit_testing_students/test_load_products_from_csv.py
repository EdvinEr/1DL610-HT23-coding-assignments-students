import csv
import os
import shutil

from checkout_and_payment import load_products_from_csv
import pytest


@pytest.fixture(scope='module')
def copy_csv_file():
    shutil.copy('products.csv', 'copy_products.csv')
    products = load_products_from_csv('copy_products.csv')
    #print("---------------------setup----------------")
    yield products
    os.remove('copy_products.csv')
    #print("-teardown--")


@pytest.fixture(scope='module')
def modify_csv_file():
    shutil.copy('products.csv', 'modify_products.csv')
    yield 'modify_products.csv'
    os.remove('modify_products.csv')


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


def test_modify_load_products_from_csv(modify_csv_file):
    with open(modify_csv_file, mode='w', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerow({'Product': 'Bread', 'Price': '-3.0', 'Units': '20'})
        writer.writerow({'Product': 'Cheese', 'Price': '3.0', 'Units': '0'})
        writer.writerow({'Product': 'Ham', 'Price': '3.0', 'Units': '-10'})

    modified_products = load_products_from_csv(modify_csv_file)

    assert modified_products[0].price == -3.0
    assert modified_products[1].units == 0
    assert modified_products[2].units == -10
