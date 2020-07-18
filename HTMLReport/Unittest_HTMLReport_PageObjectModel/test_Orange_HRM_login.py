import unittest
import HtmlTestRunner
from selenium.webdriver.common.by import By
from selenium import webdriver

class OrangeHRM_Login(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(executable_path="/home/kanik/PycharmProjects/Selenium_tutorials/drivers/chromedriver")
        cls.driver.maximize_window()

    def test_homePageTitle(self):
        self.driver.get("https://opensource-demo.orangehrmlive.com")
        self.assertEqual("OrangeHRM", self.driver.title, "Title is not same .")

    def test_login(self):
        self.driver.get("https://opensource-demo.orangehrmlive.com")
        username = self.driver.find_element(By.ID, "txtUsername")
        password = self.driver.find_element(By.ID, "txtPassword")
        login_button = self.driver.find_element(By.ID, "btnLogin")

        # Send the data to login :

        username.send_keys("Admin")
        password.send_keys("admin123")
        login_button.click()

        # Verify the login by checking the title :

        self.assertEqual("OrangeHRM11", self.driver.title, "Title is not same .")

    @classmethod
    def tearDownClass(cls) :
        cls.driver.quit()
        print("Test Completed0 ")


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="./Reports"))






