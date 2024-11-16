import logging
import os
from datetime import datetime

import colorlog
import threading  # 导入 threading 模块，方便后续获取线程相关信息

class MYLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        # 创建 logger 对象
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)  # 确保日志记录器的级别为 INFO 或更低

        # 创建控制台日志处理器
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)

        # 创建文件日志处理器
        log_dir = "./logs"
        log_file = f"app_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.fh = logging.FileHandler(os.path.join(log_dir, log_file), encoding="utf-8")
        self.fh.setLevel(logging.INFO)

        # 创建带颜色的格式化字符串
        self.formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s%(reset)s %(green)s%(asctime)s %(reset)s%(light_blue)s%(threadName)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            style='%'
        )

        # 创建文件日志格式化器（无颜色）
        self.file_formatter = logging.Formatter(
            "%(levelname)-8s %(asctime)s %(threadName)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 设置格式化器
        self.ch.setFormatter(self.formatter)
        self.fh.setFormatter(self.file_formatter)

        # 将处理器添加到 logger 中
        self.logger.addHandler(self.ch)
        self.logger.addHandler(self.fh)


def get_logger():
    return MYLogger().logger

# 测试代码
def test_function():
    logger = get_logger()
    logger.info("这是在测试函数里的日志信息")


if __name__ == "__main__":
    logger = get_logger()
    logger.info("这是主线程里的日志信息")
    thread = threading.Thread(target=test_function)
    thread.start()
    thread.join()