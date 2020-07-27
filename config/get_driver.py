import warnings
from selenium import webdriver


def get_h5_driver():
    mobile_emulation = {"deviceName": "iPhone 5/SE"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_experimental_option('w3c', False)
    warnings.simplefilter("ignore", ResourceWarning)
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_web_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


