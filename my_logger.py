import logging
import colorlog


def get_logger():
    # 创建 logger 对象
    logger = logging.getLogger(__name__)
    # 配置日志记录器的级别
    logger.setLevel(logging.INFO)  # 确保日志记录器的级别为 INFO 或更低

    # 创建 handler
    ch = logging.StreamHandler()

    # 创建带颜色的 formatter
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(green)s%(asctime)s %(reset)s%(light_blue)s%(message)s",
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
    ch.setFormatter(formatter)

    # 将 handler 添加到 logger 中
    logger.addHandler(ch)
    return logger
