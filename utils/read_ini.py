from config.PATH import *
import configparser


class ReadIni(object):

    def __init__(self, file_name):
        self.cf = configparser.ConfigParser()
        self.cf.read(file_name, encoding="utf-8-sig")

    def get_value(self, section, option):
        data = self.cf.get(section, option)
        return eval(data)


if __name__ == '__main__':
    pass
