import unittest

class PaymentTest(unittest.TestCase):

    def test_paymentIndollor(self):
        print("This is payment in Dollor Test")
        self.assertTrue(True)

    def test_paymentInrupees(self):
        print("This is payment in Rupees Test")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()