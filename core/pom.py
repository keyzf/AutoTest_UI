import datetime
import time
import win32con
import win32gui
from selenium.webdriver import TouchActions, ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from utils.read_ini import ReadIni
from utils.read_yaml import ReadYaml
import pyperclip
from utils.my_logger import log
from utils.common import *
from utils.small_tools import del_symbol
from config.PATH import TEST_SCREENSHOT


class BasePages:
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def get_ini(filename, section, option):
        log.info('读取ini文件：{} - {} - {}'.format((os.path.split(filename)[-1]), section, option))
        try:
            read = ReadIni(filename)
            return read.get_value(section, option)
        except Exception as e:
            log.info('读取ini文件 --> 错误：{}'.format(e))

    @staticmethod
    def get_yaml(filename, json_path):
        log.info('读取yaml文件：{} - {}'.format((os.path.split(filename)[-1]), json_path))
        try:
            yaml_result = ReadYaml(filename)
            return yaml_result
        except Exception as e:
            log.info('读取yaml文件 --> 错误：{}'.format(e))

    def open_url(self, url):
        """打开网址"""
        try:
            log.info('打开 {} 网址进行测试'.format(url))
            self.driver.get(url)
        except Exception as e:
            log.error('打开网址 --> 失败：{}'.format(e))
            assert False

    def get_current_url(self):
        """获取当前网址"""
        url_result = self.driver.current_url
        log.info('获取当前页面的网址为：{}'.format(url_result))
        return url_result

    def get_page_title(self):
        """获取当前网页title"""
        title_name = self.driver.title
        log.info('获取当前页面的名称为：{}'.format(title_name))
        return title_name

    def wait_presence(self, locator, timeout: int or float, timeout_shot: bool):
        """等待元素存在"""
        start = datetime.datetime.now()
        try:
            log.info('等待元素存在：{}'.format(locator))
            result = WebDriverWait(self.driver, timeout).until(ec.presence_of_all_elements_located(locator))
            success_end = datetime.datetime.now()
            success_count_time = (success_end - start).seconds
            if len(result) > 0:
                log.info('等待时长：{}s/{}s。'.format(success_count_time, timeout))
                return True
        except Exception as e:
            error_end = datetime.datetime.now()
            error_count_time = (error_end - start).seconds
            log.error('等待元素存在：{} -- {}s/{}s --> 错误：{}'.format(locator, error_count_time, timeout, e))
            if timeout_shot:
                mark = '异常截图'
                now_time = time.strftime('%Y%m%d%H%M%S')
                suffix = '.png'
                filepath = os.path.join(TEST_SCREENSHOT, mark + now_time + suffix)
                self.shot(filepath)
            return False

    def __wait_presence(self, locator, timeout: int or float):
        """等待元素存在"""
        try:
            result = WebDriverWait(self.driver, timeout).until(ec.presence_of_all_elements_located(locator))
            if len(result) > 0:
                return True
        except Exception as e:
            log.warning(e)
            return False

    def wait_visibility(self, locator, timeout: int or float):
        """等待元素可见"""
        start = datetime.datetime.now()
        try:
            log.info('等待元素可见：{}'.format(locator))
            result = WebDriverWait(self.driver, timeout).until(ec.visibility_of_all_elements_located(locator))
            success_end = datetime.datetime.now()
            success_count_time = (success_end - start).seconds
            if len(result) > 0:
                log.info('等待时长：{}s/{}s。'.format(success_count_time, timeout))
                return True
        except Exception as e:
            error_end = datetime.datetime.now()
            error_count_time = (error_end - start).seconds
            log.error('等待元素可见：{} -- {}s/{}s --> 错误：{}'.format(locator, error_count_time, timeout, e))
            return False

    @staticmethod
    def sleep(time01: int or float):
        log.info('强制等待：%d秒' % time01)
        time.sleep(time01)

    def implicitly_wait(self, time01: int or float):
        log.info('显式等待：%d' % time01)
        self.driver.implicitly_wait(time01)

    def shot(self, save_to_filepath):
        """截图"""
        try:
            log.info('截图：{}'.format(save_to_filepath))
            self.driver.save_screenshot(save_to_filepath)
        except Exception as e:
            log.error('截图：{} --> 失败：{}'.format(save_to_filepath, e))
            assert False

    def find_element(self, locator):
        """单数元素 - 定位"""
        by, element = locator
        log.info("定位单个元素: {}".format(locator))
        start = datetime.datetime.now()
        if self.__wait_presence(locator, 15):
            try:
                if by.lower() == 'id':
                    result = self.driver.find_element_by_id(element)
                elif by.lower() == 'xpath':
                    result = self.driver.find_element_by_xpath(element)
                elif by.lower() in ['class_name', 'class name']:
                    result = self.driver.find_element_by_class_name(element)
                elif by.lower() in ['css_selector', 'css selector']:
                    result = self.driver.find_element_by_css_selector(element)
                elif by.lower() in ['tag_name', 'tag name']:
                    result = self.driver.find_element_by_tag_name(element)
                elif by.lower() in ['link_text', 'link text']:
                    result = self.driver.find_element_by_link_text(element)
                elif by.lower() in ['partial_link_text', 'partial link text']:
                    result = self.driver.find_element_by_partial_link_text(element)
                else:
                    raise NameError("你选择的元素定位方式 {} 有误".format(by))
                success_end = datetime.datetime.now()
                success_count_time = (success_end - start).seconds
                spend_time = '{}s/{}s'.format(success_count_time, 15)
                log.info('耗时：{}'.format(spend_time))
                return result
            except Exception as e:
                log.error("定位失败：{}".format(e))
                mark = '异常截图'
                now_time = time.strftime('%Y%m%d%H%M%S')
                suffix = '.png'
                filepath = os.path.join(TEST_SCREENSHOT, mark + now_time + suffix)
                self.shot(filepath)
                assert False
        else:
            error_end = datetime.datetime.now()
            error_count_time = (error_end - start).seconds
            spend_time = '{}s/{}s'.format(error_count_time, 15)
            log.error('定位失败：元素不存在。耗时：{}'.format(spend_time))
            assert False

    def find_elements(self, locator):
        """复数元素 - 定位"""
        by, element = locator
        log.info("定位多个元素: {}".format(locator))
        start = datetime.datetime.now()
        if self.__wait_presence(locator, 15):
            try:
                if by.lower() == 'id':
                    result = self.driver.find_elements_by_id(element)
                elif by.lower() == 'xpath':
                    result = self.driver.find_elements_by_xpath(element)
                elif by.lower() in ['class_name', 'class name']:
                    result = self.driver.find_elements_by_class_name(element)
                elif by.lower() in ['css_selector', 'css selector']:
                    result = self.driver.find_elements_by_css_selector(element)
                elif by.lower() in ['tag_name', 'tag name']:
                    result = self.driver.find_elements_by_tag_name(element)
                elif by.lower() in ['link_text', 'link text']:
                    result = self.driver.find_elements_by_link_text(element)
                elif by.lower() in ['partial_link_text', 'partial link text']:
                    result = self.driver.find_elements_by_partial_link_text(element)
                else:
                    raise NameError("你选择的元素定位方式 {} 有误".format(by))
                success_end = datetime.datetime.now()
                success_count_time = (success_end - start).seconds
                spend_time = '{}s/{}s'.format(success_count_time, 15)
                log.info('耗时：{}'.format(spend_time))
                return result
            except Exception as e:
                log.error("定位失败：{}".format(e))
                # mark = '异常截图'
                # now_time = time.strftime('%Y%m%d%H%M%S')
                # suffix = '.png'
                # filepath = os.path.join(TEST_SCREENSHOT, mark + now_time + suffix)
                # self.shot(filepath)
                assert False
        else:
            error_end = datetime.datetime.now()
            error_count_time = (error_end - start).seconds
            spend_time = '{}s/{}s'.format(error_count_time, 15)
            log.error('定位失败：元素不存在。耗时：{}'.format(spend_time))
            assert False

    def click_element(self, locator):
        """点击元素"""
        ele = self.find_element(locator)
        try:
            log.info("点击元素")
            ele.click()
            return ele
        except Exception as e:
            log.error("点击元素 --> 失败：{}".format(e))
            assert False

    def click_svg_element(self, locator):
        ele = self.find_element(locator)
        action = ActionChains(self.driver)
        try:
            log.info("点击svg元素")
            time.sleep(1)
            action.click(ele).perform()
        except Exception as e:
            log.error("点击svg元素 --> 失败：{}".format(e))
            assert False

    def scroll_screen_click_element(self, locator):
        """屏幕滑动 - 直到某元素显示出来为止"""
        action = ActionChains(self.driver)
        ele = self.scroll_to_element(locator)
        log.info('鼠标点击')
        time.sleep(2)
        action.click(ele).perform()

    def clear_textarea(self, locator):
        """清空文本框"""
        ele = self.click_element(locator)
        try:
            action = ActionChains(self.driver)
            log.info("清空文本框")
            action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
            return ele
        except Exception as e:
            log.error("清空文本框 --> 失败：{}".format(e))
            assert False

    def input_content(self, locator, content):
        """输入内容"""
        ele = self.find_element(locator)
        try:
            log.info('输入内容："{}"'.format(content))
            ele.send_keys(content)
        except Exception as e:
            log.error('输入内容 --> 失败：{}'.format(e))
            assert False

    def clear_and_input_content(self, locator, content):
        ele = self.clear_textarea(locator)
        log.info('输入内容：{}'.format(content))
        ele.send_keys(content)

    def paste_content(self, locator, content):
        """点击文本框 并 粘贴内容"""
        pyperclip.copy(content)
        time.sleep(0.5)
        self.click_element(locator)
        try:
            action = ActionChains(self.driver)
            log.info('粘贴内容："{}"'.format(content))
            action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).send_keys(Keys.ESCAPE).perform()
        except Exception as e:
            log.error('粘贴内容 --> 失败：{}'.format(e))
            assert False

    def get_element_attribute(self, locator, attribute):
        """
        获取元素的属性
        :param locator: 元素对象
        :param attribute: 属性名字（text/id/class/tag等等）
        :return:
        """
        time.sleep(1)
        ele = self.find_element(locator)
        try:
            log.info('获取单个元素的 {}。'.format(attribute))
            if attribute.lower() == "text":
                result = ele.get_attribute('textContent')
            else:
                result = ele.get_attribute('{}'.format(attribute))
            log.info('获取到的值：{}'.format(result))
            return result
        except Exception as e:
            log.error('获取单个元素的 {} --> 失败：{}'.format(attribute, e))
            assert False

    def get_element_attribute_delSymbol(self, locator, attribute):
        """
        获取元素的属性，并且删除各种符号
        :param locator: 元素对象
        :param attribute: 属性名字（text/id/class/tag等等）
        :return:
        """
        time.sleep(1)
        ele = self.find_element(locator)
        try:
            log.info('获取单个元素的 {}，且删除所有符号。'.format(attribute))
            if attribute.lower() == "text":
                result = del_symbol(ele.get_attribute('textContent'))
            else:
                result = del_symbol(ele.get_attribute('{}'.format(attribute)))
            log.info('获取到的值：{}'.format(result))
            return result
        except Exception as e:
            log.error('获取单个元素的 {}，且删除所有符号 --> 失败：{}'.format(attribute, e))
            assert False

    def get_elements_attribute(self, locator, attribute):
        """
        获取元素的属性
        :param locator: 元素对象
        :param attribute: 属性名字（text/id/class/tag等等）
        :return:
        """
        time.sleep(1)
        ele = self.find_elements(locator)
        result = []
        try:
            log.info('获取所有元素的 {}。'.format(attribute))
            if attribute.lower() == "text":
                for i in ele:
                    attr_value = i.get_attribute('textContent')
                    result.append(attr_value)
            else:
                for i2 in ele:
                    attr_value2 = i2.get_attribute(attribute)
                    result.append(attr_value2)
            log.info('获取到的值：{}'.format(result))
            return result
        except Exception as e:
            log.error('获取所有元素的 {} --> 失败：{}'.format(attribute, e))
            assert False

    def get_elements_attribute_delSymbol(self, locator, attribute):
        """
        获取元素的属性，且删除所有符号
        :param locator: 元素对象
        :param attribute: 属性名字（text/id/class/tag等等）
        :return:
        """
        time.sleep(1)
        ele = self.find_elements(locator)
        result = []
        try:
            log.info('获取所有元素的 {}。'.format(attribute))
            if attribute.lower() == "text":
                for i in ele:
                    attr_value = del_symbol(i.get_attribute('textContent'))
                    result.append(attr_value)
            else:
                for i2 in ele:
                    attr_value2 = del_symbol(i2.get_attribute(attribute))
                    result.append(attr_value2)
            log.info('获取到的值：{}'.format(result))
            return result
        except Exception as e:
            log.error('获取所有元素的 {} --> 失败：{}'.format(attribute, e))
            assert False

    @staticmethod
    def upload_file(browser, filepath):
        """非input标签文件上传"""
        try:
            log.info('上传文件：{}'.format(filepath))
            # 窗口title
            browser_type = {
                "firefox": "文件上传",
                "chrome": "打开",
                "ie": "选择要加载的文件"
            }
            # 提升容错性
            if browser.lower() not in browser_type.keys():
                browser1 = "chrome"
            else:
                browser1 = browser
            # 正式的操作
            dialog = win32gui.FindWindow("#32770", browser_type[browser1])  # 一级窗口
            combobox_ex32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级窗口
            combobox = win32gui.FindWindowEx(combobox_ex32, 0, 'ComboBox', None)  # 三级窗口
            edit = win32gui.FindWindowEx(combobox, 0, 'Edit', None)  # 四级窗口  -->  路径输入框
            button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 四级窗口  -->  打开按钮
            win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filepath)  # 输入文件路径
            win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮
            time.sleep(1)
        except Exception as e:
            log.error('上传文件 --> 失败：{}'.format(filepath, e))
            assert False

    def scroll_up_from_element(self, start_locator, x_pixel=0, y_pixel=600):
        """
        以某个元素为起点，把屏幕向某个方向滑动
        :param start_locator: 起始元素点
        :param x_pixel: X轴的像素
        :param y_pixel: Y轴的像素
        :return:
        """
        ele = self.find_element(start_locator)
        try:
            Action = TouchActions(self.driver)
            # 从button元素的0点起始，滚动条向下（+向下，-向上）滑动700个像素 = 页面向上滑动默认的700个像素
            log.info('向上滑屏幕')
            Action.scroll_from_element(ele, x_pixel, y_pixel).perform()
        except Exception as e:
            log.error('向上滑屏幕 --> 失败：{}'.format(e))
            assert False

    def scroll_to_element(self, locator):
        ele = self.find_element(locator)
        try:
            log.info('滑动屏幕 - 元素居于屏幕最上 - 为止。')
            self.driver.execute_script('arguments[0].scrollIntoView();', ele)
            return ele
        except Exception as e:
            log.error('滑动屏幕 - 元素居于屏幕最上 - 为止 --> 失败：{}'.format(e))
            assert False

    def swipe_screen(self, x_pixel, y_pixel):
        """自定义滑动屏幕"""
        touch = TouchActions(self.driver)
        try:
            log.info('滑动屏幕：({}，{})'.format(x_pixel, y_pixel))
            touch.scroll(x_pixel, y_pixel)
        except Exception as e:
            log.error('滑动屏幕 --> 失败：{}'.format(e))
            assert False

    def swipe_up_screen(self, up_pixel: int):
        """向上滑动屏幕"""
        touch = TouchActions(self.driver)
        try:
            log.info('滑动屏幕 - 向上 {} 个像素点)'.format(up_pixel))
            touch.scroll(0, up_pixel).perform()
            # self.driver.execute_script(0, up_pixel)
        except Exception as e:
            log.error('滑动屏幕 - 向上 --> 失败：{}'.format(e))
            assert False

    def swipe_down_screen(self, down_pixel: int):
        """向下滑动屏幕"""
        touch = TouchActions(self.driver)
        try:
            log.info('滑动屏幕 - 向下 {} 个像素点)'.format(down_pixel))
            touch.scroll(0, -down_pixel).perform()
            # self.driver.execute_script('window.scrollBy("0", "{}")'.format(0-down_pixel))
        except Exception as e:
            log.error('滑动屏幕 - 向下 --> 失败：{}'.format(e))
            assert False

    def drag_element(self, locator, pixel: tuple):
        """
        :param locator: 元素定位
        :param pixel: 拖动的坐标量
        :return: 无
        """
        try:
            ele = self.find_element(locator)
            action = ActionChains(self.driver)
            log.info("拖动元素： {}".format(pixel))
            action.drag_and_drop_by_offset(ele, pixel[0], pixel[1]).perform()
        except Exception as e:
            log.info("拖动元素 --> 失败".format(e))
            assert False

    def into_dialog(self):
        """进入iframe"""

        if ec.alert_is_present():
            log.info('会话窗 存在，进入。')
            return self.driver.switch_to.alert
        else:
            log.error('会话窗 不存在。')
            return False

    def confirm_dialog(self):
        """
        会话（alert、confirm窗口）,点击确认
        :return:
        """
        alert = self.into_dialog()
        try:
            log.info('处理会话窗 --> 确认。')
            alert.accept()
        except Exception as e:
            log.error('处理会话窗 --> 确认失败：{}'.format(e))
            assert False

    def cancel_dialog(self):
        """
        会话（alert、confirm窗口）,点击取消
        :return:
        """
        alert = self.into_dialog()
        try:
            log.info('处理会话窗 --> 取消。')
            alert.dismiss()
        except Exception as e:
            log.error('处理会话窗 --> 取消失败：{}'.format(e))
            assert False

    def send_keys_dialog(self, content):
        """
        会话（prompt窗口）,点击输入内容
        :param content: 输入的内容
        :return:
        """
        alert = self.into_dialog()
        try:
            log.info('处理会话窗 --> 输入内容：{}'.format(content))
            alert.send_keys(content)
        except Exception as e:
            log.error('处理会话窗 --> 输入内容失败：{}'.format(e))
            assert False

    def get_text_dialog(self):
        """
        会话（alert、confirm、prompt窗口）,点击获取文本
        :return:
        """
        alert = self.into_dialog()
        try:
            log.info('处理会话窗 --> 获取文本。')
            alert_text = alert.text
            return alert_text
        except Exception as e:
            log.error('处理会话窗 --> 获取文本失败：{}'.format(e))
            assert False

    def into_frame(self, locator):
        """
        进入iframe
        """
        ele = self.find_element(locator)
        log.info('进入iframe：{}'.format(locator))
        self.driver.switch_to.frame(ele)

    def quit_one_frame(self):
        """
        退出一个iframe
        """
        log.info('处理frame --> 退出到上一级'.format())
        self.driver.switch_to.parent_frame()

    def quit_all_frame(self):
        """
        退出iframe，到主HTML
        """
        log.info('处理frame --> 退出到主HTML'.format())
        self.driver.switch_to.default_content()

    def current_window(self):
        """当前在第几个浏览器窗口"""
        window_handle_list = self.driver.window_handles
        current_window = window_handle_list.index[self.driver.current_window()] + 1
        log.info('浏览器窗口 --> 第{}/共{}}'.format(current_window, len(window_handle_list)))
        return current_window

    def open_new_window(self, url=None):
        """
        打开新的浏览器窗口
        :param url: 要打开的网址
        """
        js = "window.open('%s')" % url
        log.info('浏览器窗口 --> 新开 {}'.format(url))
        self.driver.execute_script(js)

    def switch_window(self, window_order: int):
        """
        进入某一个浏览器窗口
        :param window_order: 窗口下标
        """
        window_handle_list = self.driver.window_handles
        log.info('浏览器窗口 --> 第{}/共{}'.format(window_order-1, len(window_handle_list)))
        self.driver.switch_to.window(window_handle_list[window_order - 1])

    def quit_browser(self):
        log.info('浏览器 --> 退出')
        self.driver.quit()

    def back_browser(self):
        log.info('浏览器 --> 返回')
        self.driver.back()

    def refresh_browser(self):
        log.info('浏览器 --> 刷新')
        self.driver.refresh()
