from products import display_filtered_table
import os, shutil, pytest, unittest

# inputs:
# open(csv_filename, 'r', newline='') as csvfile
# display_filtered_table(csv_filename, search)

@pytest.fixture(scope='module')
def copy_csv_file():
    shutil.copy('products.csv', 'copy_products.csv')
    print("\n----------------setup----------------\n")
    yield
    os.remove('copy_products.csv')
    print("\n----------------teardown----------------\n")

# Test a non-existing file
def test_EC1():
    with pytest.raises(FileNotFoundError):
        display_filtered_table("non_existing_file.csv", "Apple")

# Test an empty csv file
def test_EC2(capsys):
    display_filtered_table("test_files/test_empty.csv", "Apple")
    out, err = capsys.readouterr()
    assert out == ""

# Test an empty string as csv file input
def test_EC3():
    with pytest.raises(FileNotFoundError):
        display_filtered_table("", "Apple")

# Test an empty string as search input
def test_EC4(capsys, copy_csv_file):
    display_filtered_table("copy_products.csv", "")
    out, err = capsys.readouterr()
    assert out == "['Product', 'Price', 'Units']\n"

# Test a csv file with only 1 column
def test_EC5(capsys):
    display_filtered_table("test_files/test_1_column.csv", "1")
    out, err = capsys.readouterr()
    assert out == "['Product']\n['1']\n"

# Test a csv file containing an empty row
def test_EC6(capsys):
    display_filtered_table("test_files/test_empty_row.csv", "Orange")
    out, err = capsys.readouterr()
    assert out == "['Product', 'Price', 'Units']\n['Orange', '1.5', '8']\n"

# Test a csv file containing different types
def test_EC7(capsys):
    display_filtered_table("test_files/test_different_types.csv", "1.0")
    out, err = capsys.readouterr()
    assert out == "['Product']\n['1.0']\n"

# Test a csv file containing 4 columns
def test_EC8(capsys):
    display_filtered_table("test_files/test_4_columns.csv", "Banana")
    out, err = capsys.readouterr()
    assert out == "['Product', 'Price', 'Units', 'Status']\n['Banana', '1', '15', '0']\n"

# Test a csv file containing varying column amounts
def test_EC9(capsys):
    display_filtered_table("test_files/test_different_column_amounts.csv", "Banana")
    out, err = capsys.readouterr()
    assert out == "['Product', 'Price', 'Units', 'Status']\n['Banana', '1']\n"

# Test a csv file not containing a 'Product' column
def test_EC10():
    with pytest.raises(ValueError):
        display_filtered_table("test_files/test_no_product_column.csv", "Banana")

# Test a csv file with 'Product' as the second column
def test_EC11(capsys):
    display_filtered_table("test_files/test_product_is_second_column.csv", "Banana")
    out, err = capsys.readouterr()
    assert out == "['Price', 'Product', 'Units']\n['1', 'Banana', '15']\n"

# Test a csv file containing varying column amounts with 'Product' as the second column
def test_EC12(capsys):
    display_filtered_table("test_files/test_varying_amounts_product_is_second.csv", "Banana")
    out, err = capsys.readouterr()
    assert out == "['Price', 'Product', 'Units']\n['1', 'Banana', '15']\n"

# Test a non-existing product
def test_EC13(capsys, copy_csv_file):
    display_filtered_table("copy_products.csv", "Pancake")
    out, err = capsys.readouterr()
    assert out == "['Product', 'Price', 'Units']\n"

def test_EC14a(capsys, copy_csv_file):
    display_filtered_table("copy_products.csv", "Apple")
    out,err=capsys.readouterr()
    assert out=="['Product', 'Price', 'Units']\n['Apple', '2', '10']\n"

def test_EC14b(capsys, copy_csv_file):
    display_filtered_table("copy_products.csv", "Dish Soap")
    out,err=capsys.readouterr()
    assert out=="['Product', 'Price', 'Units']\n['Soap', '1', '12']\n['Dish Soap', '1.5', '12']\n"

def test_EC14c(capsys, copy_csv_file):
    display_filtered_table("copy_products.csv", "Backpack")
    out,err=capsys.readouterr()
    assert out=="['Product', 'Price', 'Units']\n['Backpack', '25', '1']\n['Backpack', '15', '1']\n"