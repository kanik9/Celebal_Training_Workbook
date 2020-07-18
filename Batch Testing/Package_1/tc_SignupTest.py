import unittest

class SignupTest(unittest.TestCase):

    def test_signupByemail(self):
        print("This is Signup by Email Test")
        self.assertTrue(True)

    def test_signupByfacebook(self):
        print("This is Signup by Facebook Test")
        self.assertTrue(True)

    def test_signupBytwitter(self):
        print("This is Signup by Twitter Test")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()