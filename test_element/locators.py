from selenium.webdriver.common.by import By


class LoginElement:
    username_textbox = ('xpath', '//*[@placeholder="账号"]')
    pwd_textbox = (By.XPATH, '//*[@placeholder="密码"]')
    login_btn = (By.CLASS_NAME, 'el-button--primary')
    error_userInfo = ('xpath', '//*[contains(text(), "用户不存在/密码错误")]')
    empty_username = ('xpath', '//*[contains(text(), "用户名不能为空")]')
    empty_password = ('xpath', '//*[contains(text(), "密码不能为空")]')
