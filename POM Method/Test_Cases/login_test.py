import time
import unittest
import HtmlTestRunner
from selenium import webdriver

import sys
sys.path.append("/home/kanik/PycharmProjects/Selenium_tutorials/POM Method")
from Page_objects.login_page import LoginPage



class Login_test(unittest.TestCase):
    baseURL = "https://admin-demo.nopcommerce.com/login?ReturnUrl=%2Fadmin%2F"
    username = "admin@yourstore.com"
    password = "admin"

    driver = webdriver.Chrome(executable_path="../drivers/chromedriver")

    @classmethod
    def setUpClass(cls) :
        cls.driver.get(cls.baseURL)
        cls.driver.maximize_window()

    def test_login(self):
        login = LoginPage(self.driver)
        login.setUserName(self.username)
        login.setPassword(self.password)
        login.clickLogin()
        time.sleep(5)
        self.assertEqual("Dashboard / nopCommerce administration", self.driver.title, "Web page title is not same.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="/home/kanik/PycharmProjects/Selenium_tutorials/POM Method/Report/"))


