import threading

import my_logger
from Chrome import Chrome
from appoitment import appointment, login
from art import *



if __name__ == '__main__':
    tprint("SDUT-APPOINTMENT")
    try:
        appointment(login())
    finally:
        my_logger.MYLogger().logger.info("正在关闭浏览器...")
        Chrome().get_browser().quit()
        my_logger.MYLogger().logger.info("浏览器已经关闭")
