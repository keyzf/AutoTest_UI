from core.pom import BasePages
from test_element.locators import LoginElement as LE


class LoginPages(BasePages):

    def input_user_info(self, phone, password):
        self.clear_and_input_content(LE.username_textbox, phone)
        self.clear_and_input_content(LE.pwd_textbox, password)

    def click_logbtn(self):
        self.click_element(LE.login_btn)

    def check_login(self, locator):
        return self.wait_presence(locator, 2, True)

