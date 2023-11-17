import csv
import os
import shutil

from checkout_and_payment import load_products_from_csv
import pytest

#def test_int_input():
#    assert load_products_from_csv(1) == "Input is not a csv file"

#def test_float_input():
#    assert load_products_from_csv(0.5) == "Input is not a csv file"

#def test_list_input():
#    assert load_products_from_csv(["csvfile"]) == "Input is not a csv file"

#def test_string_input():
#    assert load_products_from_csv("csv") == "Input is not a csv file"

#def test_EC1():
#    assert load_products_from_csv("non_valid_csv") == "Input is not a valid csv file"

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


def test_1_load_products_from_csv(copy_csv_file):
    products = copy_csv_file
    assert products[0].name == 'Apple'
    assert products[0].price == 2.0
    assert products[0].units == 10

    assert products[1].name == 'Banana'
    assert products[1].price == 1.0
    assert products[1].units == 15


def test_2_modify_load_products_from_csv(modify_csv_file):
    #Negative or no price
    with open(modify_csv_file, mode='w', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerow({'Product': 'Bread', 'Price': '-3.0', 'Units': '20'})
        writer.writerow({'Product': 'Ham', 'Price': '0', 'Units': '0'})

    modified_products = load_products_from_csv(modify_csv_file)

    assert modified_products[0].price == -3.0
    assert modified_products[1].price == 0

def test_3_modify_load_products_from_csv(modify_csv_file):
    #Negative or no units
    with open(modify_csv_file, mode='w', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerow({'Product': 'Fries', 'Price': '3.0', 'Units': '-10'})
        writer.writerow({'Product': 'Popcorn', 'Price': '4.0', 'Units': '0'})

    modified_products = load_products_from_csv(modify_csv_file)
    assert modified_products[0].units == -10
    assert modified_products[1].units == 0


def test_4_modify_load_products_from_csv(modify_csv_file):
    # No name as string
    with open(modify_csv_file, mode='w', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerow({'Product': 1, 'Price': '3.0', 'Units': '-10'})
        writer.writerow({'Product': 0.5, 'Price': '4.0', 'Units': '0'})

    modified_products = load_products_from_csv(modify_csv_file)
    #print(type(modified_products[0].name))
    assert modified_products[0].name == '1'
    assert modified_products[1].name == '0.5'


def test_5_modify_load_products_from_csv(modify_csv_file):
    # Empty CSV file
    with open(modify_csv_file, mode='w', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

    modified_products = load_products_from_csv(modify_csv_file)
    assert modified_products == []


def test_6_modify_load_products_from_csv(modify_csv_file):
    # CSV file with empty row "in the middle"
    with open(modify_csv_file, mode='w', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerow({'Product': 1, 'Price': '3.0', 'Units': '-10'})
        writer.writerow({'Product': 'Popcorn', 'Price': '4.0', 'Units': '0'})

    modified_products = load_products_from_csv(modify_csv_file)
    #print(modified_products[0].name)


def test_7_modify_load_products_from_csv(modify_csv_file):
    # CSV file with more than three columns
    with open(modify_csv_file, mode='w', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerow({'Product': 1, 'Price': '3.0', 'Units': '-10'})
        writer.writerow({'Product': 'Popcorn', 'Price': '4.0', 'Units': '0'})

    modified_products = load_products_from_csv(modify_csv_file)
    #print(modified_products[0].name)