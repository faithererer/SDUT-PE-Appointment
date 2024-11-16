import signal
import sys
import threading
from gbl import *
import config_reader
import my_logger
from AppoiintmentType import AppointmentType
from Chrome import Chrome
from appoitment import appointment, login
from art import *
from use_api import *


if __name__ == '__main__':
    def graceful_exit(signal_num, frame):
        sys.exit(0)

    # 捕获 Ctrl+C 信号
    signal.signal(signal.SIGINT, graceful_exit)
    tprint("SDUT-APPOINTMENT")
    try:
        if config_reader.get_mode() == "1":
            appointment("用户登录")
        elif config_reader.get_mode() == "2":
            if config_reader.get_policy() == "1":
                appointment_by_api(AppointmentType.INNER, requests.session())
            elif config_reader.get_policy() == "2":
                appointment_by_api(AppointmentType.OUTER, requests.session())
            elif config_reader.get_policy() == "3":
                lock = threading.Lock()
                t1 = threading.Thread(target=appointment_by_api,
                                      args=(AppointmentType.INNER, requests.session(), True, lock))
                t2 = threading.Thread(target=appointment_by_api,
                                      args=(AppointmentType.OUTER, requests.session(), True, lock))
                t1.start()
                t2.start()
                try:
                    # 循环等待线程完成，允许捕获中断
                    while t1.is_alive() or t2.is_alive():
                        t1.join(timeout=0.1)
                        t2.join(timeout=0.1)
                except KeyboardInterrupt:
                    logger.info("程序被用户中断")
                    raise
            else:
                my_logger.get_logger().error("policy配置错误")
        else:
            my_logger.get_logger().error("mode配置错误")
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    finally:
        logger.info("预约结果:室内:"+str(result[AppointmentType.INNER])+"室外:"+str(result[AppointmentType.OUTER]))
        my_logger.MYLogger().logger.info("正在关闭浏览器...")
        Chrome().get_browser().quit()
        my_logger.MYLogger().logger.info("浏览器已经关闭")
