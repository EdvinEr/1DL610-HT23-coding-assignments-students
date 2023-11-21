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

def test_int_input():
    assert load_products_from_csv(1)

def test_float_input():
    assert load_products_from_csv(0.5)

def test_list_input():
    assert load_products_from_csv(["copy_products.csv"])

def test_string_input():
    assert load_products_from_csv("copy_products.csv")

def test_EC1():
    assert load_products_from_csv("non_valid.csv")

#def test_EC2():
    #tom string
    #Tom csv fil
    #En kolumn
    #En csv med en tom rad


def test_1_load_products_from_csv(copy_csv_file):
    products = copy_csv_file
    assert products[0].name == 'Apple'
    assert products[0].price == 2.0
    assert products[0].units == 10

    assert products[1].name == 'Banana'
    assert products[1].price == 1.0
    assert products[1].units == 15

def test_2_load_products_from_csv(copy_csv_file):
    products = copy_csv_file
    expected_length = 71

    assert len(products) == expected_length

def test_3_modify_load_products_from_csv(modify_csv_file):
    #Negative or no price
    with open(modify_csv_file, mode='a', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        csvfile.write('\n')
        writer.writerow({'Product': 'Bread', 'Price': '-3.0', 'Units': '20'})
        writer.writerow({'Product': 'Ham', 'Price': '0', 'Units': '10'})

    modified_products = load_products_from_csv(modify_csv_file)

    assert modified_products[71].price == -3.0
    assert modified_products[72].price == 0

def test_4_modify_load_products_from_csv(modify_csv_file):
    #Negative or no units
    with open(modify_csv_file, mode='a', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow({'Product': 'Fries', 'Price': '3.0', 'Units': '-10'})
        writer.writerow({'Product': 'Popcorn', 'Price': '4.0', 'Units': '0'})

    modified_products = load_products_from_csv(modify_csv_file)
    assert modified_products[73].units == -10
    assert modified_products[74].units == 0


def test_5_modify_load_products_from_csv(modify_csv_file):
    # No name as string
    with open(modify_csv_file, mode='a', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow({'Product': 1, 'Price': '3.0', 'Units': '-10'})
        writer.writerow({'Product': 0.5, 'Price': '4.0', 'Units': '3'})

    modified_products = load_products_from_csv(modify_csv_file)
    #print(type(modified_products[0].name))
    assert modified_products[75].name == '1'
    assert modified_products[76].name == '0.5'


def test_6_modify_load_products_from_csv(modify_csv_file):
    # CSV file with empty row "in the middle"
    with open(modify_csv_file, mode='a', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow({'Product': 'Cheese', 'Price': '3.0', 'Units': '10'})
        csvfile.write('\n')
        writer.writerow({'Product': 'Popcorn', 'Price': '4.0', 'Units': '5'})

    modified_products = load_products_from_csv(modify_csv_file)

    assert modified_products[77].name == 'Cheese'
    assert modified_products[78].name == 'Popcorn'


def test_7_modify_load_products_from_csv(modify_csv_file):
    # CSV file with one less column
    with open(modify_csv_file, mode='w', newline='') as csvfile:
        fields = ['Product', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerow({'Product': 'Cheese', 'Price': '3.0'})

    with pytest.raises(KeyError):
        modified_products = load_products_from_csv(modify_csv_file)


def test_8_modify_load_products_from_csv(modify_csv_file):
    # CSV file with one more column
    with open(modify_csv_file, mode='w', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units', 'Category']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerow({'Product': 'Cheese', 'Price': '3.0', 'Units': '4', 'Category': 'Dairy'})
        writer.writerow({'Product': 'Popcorn', 'Price': '4.0', 'Units': '3', 'Category': 'Snacks'})

    modified_products = load_products_from_csv(modify_csv_file)

    assert modified_products[0].name == 'Cheese'
    assert modified_products[0].price == 3.0
    assert modified_products[0].units == 4

    assert len(modified_products[0].__dict__) == 3


def test_9_modify_load_products_from_csv(modify_csv_file):
    # CSV file with values with whitespaces
    with open(modify_csv_file, mode='w', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units', 'Category']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerow({'Product': 'Bread ', 'Price': ' 3.0 ', 'Units': ' 6 '})

    modified_products = load_products_from_csv(modify_csv_file)

    assert modified_products[0].name == 'Bread '
    assert modified_products[0].price == 3.0
    assert modified_products[0].units == 6


def test_10_modify_load_products_from_csv(modify_csv_file):
    # Empty CSV file
    with open(modify_csv_file, mode='w', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        csvfile.write('\n')

    modified_products = load_products_from_csv(modify_csv_file)

    assert modified_products == []
    assert len(modified_products) == 0
