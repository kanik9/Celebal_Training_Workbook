import unittest

from Package_1.tc_logintest import LoginTest
from Package_1.tc_SignupTest import SignupTest

from Package_2.tc_PaymentTest import PaymentTest
from Package_2.tc_paymentreturns import PaymentReturnTest


tc_1 = unittest.TestLoader().loadTestsFromTestCase(LoginTest)
tc_2 = unittest.TestLoader().loadTestsFromTestCase(SignupTest)
tc_3 = unittest.TestLoader().loadTestsFromTestCase(PaymentTest)
tc_4 = unittest.TestLoader().loadTestsFromTestCase(PaymentReturnTest)

# creating Test Suites

sanatyTestSuite = unittest.TestSuite([tc_1, tc_2])

functionalTestSuite = unittest.TestSuite([tc_3, tc_4])

MasterTestSuite = unittest.TestSuite([tc_1, tc_2, tc_3, tc_4])
print("Sanaty Test Suite : ")
unittest.TextTestRunner().run(sanatyTestSuite)
print()
print("Functional Test Suites : ")
unittest.TextTestRunner().run(functionalTestSuite)
print()
print("Master Test Suites : ")
unittest.TextTestRunner().run(MasterTestSuite)



