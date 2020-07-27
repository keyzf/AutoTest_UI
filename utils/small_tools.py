import random
import os
import time
import re


def randint(min_num, max_num):
    """
    随机整数
    :param min_num: 最小数
    :param max_num: 最大数
    :return: 随机整数
    """
    return random.randint(min_num, max_num)


def rand_float(min_num, max_num, decimal_count=None):
    """随机浮点数，可以选择精度"""
    result = random.uniform(min_num, max_num)
    if decimal_count:
        return round(result, decimal_count)
    else:
        return result


def rand_count_str(str_count):
    """随机数量的字符串"""
    rand_str = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', str_count)
    return ''.join(rand_str)


def path_join(path, *paths):
    """
    目录拼接
    :param path: 被拼接的路径
    :param paths: 需要拼接的路径
    :return: 适用于win10+、Linux的目录路径
    """
    path_result = os.path.join(path, *paths)
    return path_result.replace('\\', '/')


def change_to_windows_path(path):
    """windows系统的可用路径"""
    return path.replace('/', '\\')


def get_date(date_format: str):
    """
    :param date_format: 时间合适
    :return: 带格式的时间
    """
    return time.strftime(date_format, time.localtime(time.time()))


class GlobalA:
    A = None


def set_value(value_name, value):
    return setattr(GlobalA, value_name, value)


def has_value(value_name):
    return hasattr(GlobalA, value_name)


def get_value(value_name):
    if has_value(value_name):
        return getattr(GlobalA, value_name)
    else:
        raise Exception('没有该变量{}'.format(value_name))


def retain_int(value):
    """只保留数字"""
    return int(re.sub(r'[^\d]+', '', value))


def del_symbol(value):
    """
    祛除所有非非中文和英文和阿拉字符
    例如： 符号、空格、换行符等等
    """
    return re.sub(r'[^\w\u4e00-\u9fff]+', '', value)

