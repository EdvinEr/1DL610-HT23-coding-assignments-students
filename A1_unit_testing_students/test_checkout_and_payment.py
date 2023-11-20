from checkout_and_payment import checkoutAndPayment
from logout import logout
import pytest
import shutil
import os

print("Current working directory:", os.getcwd())
print("Directory contents:", os.listdir())

@pytest.fixture(scope='module')
def copy_json_file():
    shutil.copy('users.json', 'copy_user.json')
    print("-----------------setup------------------")
    yield
    os.remove('copy_users.json')
    print("----------------teardown----------------")

@pytest.fixture
def check_cart_stub1(mocker):
    return mocker.patch('checkout_and_payment.check_cart', return_value=False)

@pytest.fixture
def check_cart_stub2(mocker):
    return mocker.patch('checkout_and_payment.check_cart', return_value=None)

@pytest.fixture
def logout_stub1(mocker):
    return mocker.patch('logout.logout', return_value=True)

@pytest.fixture
def logout_stub2(mocker):
    return mocker.patch('logout.logout', return_value=False)

def mimic_input(input_lst):
    i = 0

    def _mimic_input(some_input):
        nonlocal i
        mimicked_input = input_lst[i]
        i += 1
        return mimicked_input
    return _mimic_input



def test_choice_add_item(logout_stub1, capsys, monkeypatch): #Not done
    login_info = {"username": "Ramanathan", "wallet": 100}
    monkeypatch.setattr("builtins.input", mimic_input(["28", "l"]))
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()
    expected_output = "Ice cream added to your cart"
    assert expected_output in out[2217:2249]
def test_choice_other_letter(logout_stub1, capsys, monkeypatch):
    login_info = {"username": "Ramanathan", "wallet": 100}
    monkeypatch.setattr("builtins.input", mimic_input(["a", "l"]))
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()
    expected_output = "Invalid input. Please try again."
    assert expected_output in out[2217:2249]

def test_choice_other_number(capsys, monkeypatch):           #händer inget??
    login_info = {"username": "Ramanathan", "wallet": 100}
    monkeypatch.setattr("builtins.input", mimic_input(["72", "l"]))
    checkoutAndPayment(login_info)
    out, err = capsys.readouterr()
    expected_output = "Invalid input. Please try again."
    assert expected_output in out[2217:2249]