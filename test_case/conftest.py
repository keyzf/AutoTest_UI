import pytest
from test_object.common_pages import LoginPages
from utils.my_logger import log
from config.get_driver import get_web_driver
from utils.read_yaml import ReadYaml

yaml_data = ReadYaml().get_yaml()
url = yaml_data["URL"]["test"]


@pytest.fixture(scope='class')
def browser_setup():
    driver = get_web_driver()
    lg = LoginPages(driver)
    lg.open_url(url)

    # 分割线：上面是setup，下面是teardown
    # 分割线（固定写法） 跟 返回值
    yield lg

    lg.quit_browser()


@pytest.fixture
def case_setup():
    log.info('')
    log.info('<' * 50 + '   用例开始   ' + '>' * 50)

    yield

    log.info('<' * 50 + '   用例结束   ' + '>' * 50)

