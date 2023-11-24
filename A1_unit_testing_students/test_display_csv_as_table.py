from products import display_csv_as_table
import os, shutil, pytest

@pytest.fixture(scope='module')
def copy_csv_file():
    shutil.copy('products.csv', 'copy_products.csv')
    print("\n----------------setup----------------\n")
    yield
    os.remove('copy_products.csv')
    print("\n----------------teardown----------------\n")

def test_int_input():
    with pytest.raises(TypeError):
        display_csv_as_table(1)

def test_float_input():
    with pytest.raises(TypeError):
        display_csv_as_table(0.5)

def test_list_input(copy_csv_file):
    with pytest.raises(TypeError):
        display_csv_as_table(["copy_products.csv", "copy_products.csv"])

# Test a non-existing file
def test_EC1():
    with pytest.raises(FileNotFoundError):
        display_csv_as_table("non_existing_file.csv")

# Test an empty csv file
def test_EC2(capsys):
    display_csv_as_table("test_files/test_empty.csv")
    out, err = capsys.readouterr()
    assert out == ""

# Test an empty string as input
def test_EC3():
    with pytest.raises(FileNotFoundError):
        display_csv_as_table("")

# Test a csv file with only 1 column
def test_EC4(capsys):
    display_csv_as_table("test_files/test_1_column.csv")
    out, err = capsys.readouterr()
    assert out == "['Product']\n['0']\n['1']\n['2']\n['3']\n['4']\n"

# Test a csv file containing an empty row
def test_EC5(capsys):
    display_csv_as_table("test_files/test_empty_row.csv")
    out, err = capsys.readouterr()
    assert out[73:75] == "[]"

# Test a csv file containing different types
def test_EC6(capsys):
    display_csv_as_table("test_files/test_different_types.csv")
    out, err = capsys.readouterr()
    assert out == "['Product']\n['Apple']\n['2']\n['1.0']\n['[1', '2', '3]']\n['[a', 'b', 'c]']\n"

# Test a csv file containing 4 columns
def test_EC7(capsys):
    display_csv_as_table("test_files/test_4_columns.csv")
    out, err = capsys.readouterr()
    assert out[0:39] == "['Product', 'Price', 'Units', 'Status']"
    assert out[40:65] == "['Apple', '2', '10', '1']"
    assert out[66:92] == "['Banana', '1', '15', '0']"
    assert out[93:120] == "['Orange', '1.5', '8', '0']"

# Test a csv file containing varying column amounts
def test_EC8(capsys):
    display_csv_as_table("test_files/test_different_column_amounts.csv")
    out, err = capsys.readouterr()
    assert out[0:39] == "['Product', 'Price', 'Units', 'Status']"
    assert out[40:49] == "['Apple']"
    assert out[50:65] == "['Banana', '1']"
    assert out[66:88] == "['Orange', '1.5', '8']"

def test_EC9(capsys, copy_csv_file):
    display_csv_as_table("copy_products.csv")
    out,err=capsys.readouterr()
    assert out[0:29]=="['Product', 'Price', 'Units']"
    assert out[30:50] == "['Apple', '2', '10']"
    assert out[51:72] == "['Banana', '1', '15']"
    assert out[73:95] == "['Orange', '1.5', '8']"
    assert out[96:116] == "['Grapes', '3', '5']"