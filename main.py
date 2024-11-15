import threading

import config_reader
import my_logger
from AppoiintmentType import AppointmentType
from Chrome import Chrome
from appoitment import appointment, login
from art import *
from use_api import *


if __name__ == '__main__':
    tprint("SDUT-APPOINTMENT")
    try:
        if config_reader.get_mode()=="1":
            appointment(login())
        elif config_reader.get_mode()=="2":
            # 根据policy判断是内部还是外部config_reader.get_policy()
            if config_reader.get_policy() == "1":
                appointment_by_api(AppointmentType.INNER, requests.session())
            elif config_reader.get_policy() == "2":
                appointment_by_api(AppointmentType.OUTER, requests.session())
            elif config_reader.get_policy() == "3":
                lock = threading.Lock()
                threading.Thread(target=appointment_by_api, args=(AppointmentType.INNER, requests.session(), True, lock)).start()
                threading.Thread(target=appointment_by_api, args=(AppointmentType.OUTER, requests.session(), True, lock)).start()
            else:
                my_logger.get_logger().error("policy配置错误")
        else:
            my_logger.get_logger().error("mode配置错误")
    finally:
        my_logger.MYLogger().logger.info("正在关闭浏览器...")
        Chrome().get_browser().quit()
        my_logger.MYLogger().logger.info("浏览器已经关闭")
        pass
