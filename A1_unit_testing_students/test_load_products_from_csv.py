import csv
import os
import shutil

from checkout_and_payment import load_products_from_csv
import pytest

@pytest.fixture(scope='module')
def copy_csv_file():
    shutil.copy('products.csv', 'copy_products.csv')
    products = load_products_from_csv('copy_products.csv')
    print("----------setup----------")
    yield products
    os.remove('copy_products.csv')
    print("----------teardown----------")

@pytest.fixture(scope='module')
def empty_csv_file():
    empty_products = 'empty_products.csv'

    with open(empty_products, 'w', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
    products = load_products_from_csv(empty_products)
    print("----------setup----------")
    yield products
    os.remove(empty_products)
    print("----------teardown----------")

@pytest.fixture(scope='module')
def modify_csv_file():
    shutil.copy('products.csv', 'modify_products.csv')
    yield 'modify_products.csv'
    os.remove('modify_products.csv')

def test_int_input():
    with pytest.raises(TypeError):
        assert load_products_from_csv(1)

def test_float_input():
    with pytest.raises(TypeError):
        load_products_from_csv(0.5)

def test_list_input(copy_csv_file):
    with pytest.raises(TypeError):
        load_products_from_csv(["copy_products.csv"])

def test_string_input():
    assert load_products_from_csv("copy_products.csv")

#Test a non-existing file
def test_EC1():
    with pytest.raises(FileNotFoundError):
        assert load_products_from_csv("non_existing.csv")

#Test an empty csv file
def test_EC2(empty_csv_file):
    empty_products = empty_csv_file
    assert len(empty_products) == 0
    assert empty_products == []

#Test an empty string as input
def test_EC3():
    with pytest.raises(FileNotFoundError):
        load_products_from_csv("")

#Test correct output
def test_EC4(copy_csv_file):
    products = copy_csv_file
    assert products[0].name == 'Apple'
    assert products[0].price == 2.0
    assert products[0].units == 10

    assert products[1].name == 'Banana'
    assert products[1].price == 1.0
    assert products[1].units == 15

    expected_length = 71
    assert len(products) == expected_length

#Test when products have negative or no price
def test_EC5(modify_csv_file):
    with open(modify_csv_file, mode='a', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        csvfile.write('\n')
        writer.writerow({'Product': 'Bread', 'Price': '-3.0', 'Units': '20'})
        writer.writerow({'Product': 'Ham', 'Price': '0', 'Units': '10'})

    modified_products = load_products_from_csv(modify_csv_file)

    assert modified_products[71].price == -3.0
    assert modified_products[72].price == 0

#Test when products have negative or no units
def test_EC6(modify_csv_file):
    with open(modify_csv_file, mode='a', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow({'Product': 'Fries', 'Price': '3.0', 'Units': '-10'})
        writer.writerow({'Product': 'Popcorn', 'Price': '4.0', 'Units': '0'})

    modified_products = load_products_from_csv(modify_csv_file)
    assert modified_products[73].units == -10
    assert modified_products[74].units == 0

#Test when products have integer or floats as name
def test_EC7(modify_csv_file):
    with open(modify_csv_file, mode='a', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow({'Product': 1, 'Price': '3.0', 'Units': '10'})
        writer.writerow({'Product': 0.5, 'Price': '4.0', 'Units': '3'})

    modified_products = load_products_from_csv(modify_csv_file)
    assert modified_products[75].name == '1'
    assert modified_products[76].name == '0.5'

#Test when CSV file has an empty row between products
def test_EC8(modify_csv_file):
    with open(modify_csv_file, mode='a', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow({'Product': 'Cheese', 'Price': '3.0', 'Units': '10'})
        csvfile.write('\n')
        writer.writerow({'Product': 'Popcorn', 'Price': '4.0', 'Units': '5'})

    modified_products = load_products_from_csv(modify_csv_file)
    assert modified_products[77].name == 'Cheese'
    assert modified_products[78].name == 'Popcorn'

#Test when CSV file has one less column
def test_EC9(modify_csv_file):
    with open(modify_csv_file, mode='w', newline='') as csvfile:
        fields = ['Product', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerow({'Product': 'Cheese', 'Price': '3.0'})

    with pytest.raises(KeyError):
        modified_products = load_products_from_csv(modify_csv_file)

#Test when CSV file has one more column
def test_EC10(modify_csv_file):
    with open(modify_csv_file, mode='w', newline='') as csvfile:
        fields = ['Product', 'Price', 'Units', 'Category']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerow({'Product': 'Cheese', 'Price': '3.0', 'Units': '4', 'Category': 'Dairy'})
        writer.writerow({'Product': 'Popcorn', 'Price': '4.0', 'Units': '3', 'Category': 'Snacks'})

    modified_products = load_products_from_csv(modify_csv_file)
    assert not any('Dairy' in str(product) for product in modified_products)

#Test when product has whitespaces in CSV file
def test_EC11(modify_csv_file):
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


