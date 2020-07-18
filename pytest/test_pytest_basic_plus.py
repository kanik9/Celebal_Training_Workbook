import pytest

"""
The purpose of test fixture is to provide a fixed baseline upon which test can reliably and repeatedly execute

1. @pytest.fixture() : Executes Specific method before every test method

2. @pytest.yield_fixture() : Executes Specific method before & After every test method
"""
@pytest.fixture()
def Setup():
    print("Once before every test method")

def test_Method_1(Setup):
    print("Hello This is test method 1")


def test_Method_2():
    print("Hello This is test method 2")