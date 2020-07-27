import logging
from config.PATH import *
import time
from utils.common import *
from utils.read_yaml import ReadYaml

day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
file = os.path.join(TEST_LOG, '{}.log'.format(day))

yaml_data = ReadYaml(YAML).get_yaml()


class MyLog:
    def __init__(self,
                 module_name,
                 all_level="DEBUG",
                 stream_level="INFO",
                 file_level="INFO",
                 all_format="[%(asctime)s] %(levelname)s [%(filename)s, %(lineno)d] %(message)s",
                 date_format="%Y-%m-%d %H:%M:%S",
                 log_file=file):
        if not os.path.exists(TEST_LOG):
            os.mkdir(TEST_LOG)  # 创建测试日志目录
        if not os.path.exists(log_file):
            open(log_file, 'w')  # 创建测试日志文件
        self.logger = logging.getLogger(module_name)  # log收集器
        self.logger.setLevel(all_level)  # 定义收集器的信息级别
        self.log_format = logging.Formatter(
            fmt=all_format,
            datefmt=date_format)  # 定义日志的格式
        # 控制台输出日志
        self.ch = logging.StreamHandler()  # 控制台输出句柄
        self.ch.setFormatter(self.log_format)  # 控制台输出的信息格式
        self.ch.setLevel(stream_level)  # 控制台输出的信息级别

        # 文件输出日志
        self.fh = logging.FileHandler(filename=log_file, mode='a', encoding='utf-8')  # mode='a' 追加写入模式
        self.fh.setFormatter(self.log_format)  # 文件输出的信息格式
        self.fh.setLevel(file_level)  # 文件输出的信息级别

        # 加载输出句柄
        self.logger.addHandler(self.ch)  # 把流媒体添加到控制台输出句柄内
        self.logger.addHandler(self.fh)

    def __del__(self):
        self.delete_handle()

    def get_logger(self):
        return self.logger

    def delete_handle(self):
        # 移除输出句柄,避免重复输出
        self.logger.removeHandler(self.ch)
        self.logger.removeHandler(self.fh)

        # 关闭 .log 文件，释放内存
        self.ch.close()
        self.fh.close()


my_logger = MyLog(module_name=get_module_name(),
                  all_level=yaml_data["logger"]["all_level"],
                  stream_level=yaml_data["logger"]["stream_level"],
                  file_level=yaml_data["logger"]["file_level"],
                  all_format=yaml_data["logger"]["all_format"],
                  date_format=yaml_data["logger"]["date_format"])
log = my_logger.get_logger()


if __name__ == '__main__':
    # log.debug("输出一个debug")
    # log.info("输出一个info")
    # log.warning("输出一个warning")
    # log.error("输出一个error")
    pass
