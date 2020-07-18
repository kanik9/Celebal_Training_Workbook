import unittest

class LoginTest(unittest.TestCase):

    def test_loginByemail(self):
        print("This is login by Email Test")
        self.assertTrue(True)

    def test_loginByfacebook(self):
        print("This is login by Facebook Test")
        self.assertTrue(True)

    def test_loginBytwitter(self):
        print("This is login by Twitter Test")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()