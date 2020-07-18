import pytest

@pytest.yield_fixture()
def Setup():
    print("Opening URL to Login")
    yield
    print("Closing browser after Loging")


def test_loginByemail(Setup):
    print("This is login by Email Test")



def test_loginByfacebook(Setup):
    print("This is login by Facebook Test")







"""
Output : 

rootdir: /home/kanik/PycharmProjects/Selenium_tutorials/pytest
collected 2 items                                               

Batch Testcases/Package_1/test_login.py::test_loginByemail Opening URL to Login
This is login by Email Test
PASSEDClosing browser after Loging

Batch Testcases/Package_1/test_login.py::test_loginByfacebook Opening URL to Login
This is login by Facebook Test
PASSEDClosing browser after Loging

"""


