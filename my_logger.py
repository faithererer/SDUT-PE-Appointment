import logging
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
        # 配置日志记录器的级别
        self.logger.setLevel(logging.INFO)  # 确保日志记录器的级别为 INFO 或更低

        # 创建 handler
        self.ch = logging.StreamHandler()

        # 创建带颜色的格式化字符串，添加线程相关信息显示，这里使用 %(threadName)s 显示线程名称，也可以使用 %(thread)d 显示线程 ID
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
            secondary_log_colors={},
            style='%'
        )

        # 为 handler 设置 formatter
        self.ch.setFormatter(self.formatter)

        # 将 handler 添加到 logger 中
        self.logger.addHandler(self.ch)


def get_logger():
    return MYLogger().logger

# 以下是测试代码示例，用于展示添加线程信息后的日志打印效果
def test_function():
    logger = get_logger()
    logger.info("这是在测试函数里的日志信息")


if __name__ == "__main__":
    logger = get_logger()
    logger.info("这是主线程里的日志信息")
    thread = threading.Thread(target=test_function)
    thread.start()
    thread.join()