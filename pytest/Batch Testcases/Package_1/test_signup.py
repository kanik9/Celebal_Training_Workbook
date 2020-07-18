import pytest


@pytest.yield_fixture()
def Setup():
    print("Opening URL to Signup")
    yield
    print("Clossing Browser after Signup")


def test_signupByemail(Setup):
    print("This is Signup by Email Test")



def test_signupByfacebook(Setup):
    print("This is Signup by Facebook Test")


"""
Output :

====================== test session starts ======================
platform linux -- Python 3.8.2, pytest-5.4.3, py-1.9.0, pluggy-0.13.1 -- /home/kanik/PycharmProjects/Selenium_tutorials/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/kanik/PycharmProjects/Selenium_tutorials/pytest/Batch Testcases/Package_1
collected 2 items                                               

test_signup.py::test_signupByemail Opening URL to Signup
This is Signup by Email Test
PASSEDClossing Browser after Signup

test_signup.py::test_signupByfacebook Opening URL to Signup
This is Signup by Facebook Test
PASSEDClossing Browser after Signup


======================= 2 passed in 0.01s =======================
"""