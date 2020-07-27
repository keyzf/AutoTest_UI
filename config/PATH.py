import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = os.path.join(PROJECT_PATH, 'config', 'config.ini')
YAML = os.path.join(PROJECT_PATH, 'config', 'config.yml')
CORE = os.path.join(PROJECT_PATH, 'core')
ALLURE_REPORT = os.path.join(PROJECT_PATH, 'output', 'test_report')
TEST_LOG = os.path.join(PROJECT_PATH, 'output', 'test_log')
ALLURE_RESULT = os.path.join(PROJECT_PATH, 'output', 'allure_report_resource')
TEST_SCREENSHOT = os.path.join(PROJECT_PATH, 'output', 'test_screenshot')
TEST_CASE = os.path.join(PROJECT_PATH, 'test_case')
TEST_DATA_FILE = os.path.join(PROJECT_PATH, 'test_data', 'file')
TEST_DATA_PARAM = os.path.join(PROJECT_PATH, 'test_data', 'param')
TEST_ELEMENT = os.path.join(PROJECT_PATH, 'test_element')
TEST_OBJECT = os.path.join(PROJECT_PATH, 'test_object')
UTILS = os.path.join(PROJECT_PATH, 'utils')
