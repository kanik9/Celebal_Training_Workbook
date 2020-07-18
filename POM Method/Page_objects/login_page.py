

class LoginPage():
    # Locators of all the element
    user_email_id = "Email"
    user_password_id = "Password"
    login_button_xpath = "/html/body/div[6]/div/div/div/div/div[2]/div[1]/div/form/div[3]/input"
    link_logout_linktext = "Logout"

    def __init__(self,driver):
        self.driver = driver

    def setUserName(self,username):
        self.driver.find_element_by_id(self.user_email_id).clear()
        self.driver.find_element_by_id(self.user_email_id).send_keys(username)

    def setPassword(self, password):
        self.driver.find_element_by_id(self.user_password_id).clear()
        self.driver.find_element_by_id(self.user_password_id).send_keys(password)

    def clickLogin(self):
        self.driver.find_element_by_xpath(self.login_button_xpath).click()

    def clickLogout(self):
        self.driver.find_element_by_xpath(self.link_logout_linktext).click()

