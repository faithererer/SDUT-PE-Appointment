import os
import random
import time
import sys
from DrissionPage import ChromiumPage
from config_reader import load_config
import CONSTRANTS
import my_logger

logger = my_logger.get_logger()


def auth_sdut():
    i = 1
    try:
        page = ChromiumPage()
    except Exception as e:
        logger.error(f"初始化浏览器或打开登录页面出错: {e}")
        return False, None

    while True:
        logger.info(f"第{i}次尝试")
        i += 1
        try:
            page.get(CONSTRANTS.AUTH_URL)
        except TimeoutError as e:
            logger.warning("您的网络可能有问题.., 请检查网络连接")
            continue

        # 获得体测系统的用户名和密码输入框
        try:
            username_ipt = page.ele('#username')
            password_ipt = page.ele('#password')
        except Exception as e:
            logger.error(f"找不到用户名或密码输入框: {e}")
            try:
                logger.info("尝试注销")
                logout(page)
                logger.info("注销成功")
            except TimeoutError as e:
                logger.error(f"注销失败,可能是网络问题: {e}")
            continue

        # 输入用户名和密码
        options = load_config()
        username = options.get('DEFAULT', 'sdut_account')
        password = options.get('DEFAULT', 'sdut_pwd')

        try:
            # 清除
            username_ipt.clear()
            username_ipt.input(username)
            # 400-600ms
            time.sleep(random.randint(1, 2))
            password_ipt.clear()
            password_ipt.input(password)
        except Exception as e:
            logger.error(f"输入用户名或密码出错: {e}")
            continue

        # 点击登录按钮
        try:
            login_btn = page.ele('#login_submit')
            login_btn.click()
        except Exception as e:
            logger.error(f"找不到或无法点击登录按钮: {e}")
            continue

        logger.info("结果")
        try:
            info = page.ele('xpath://*[@id="app"]/div[1]/div/div/div/div[2]/div[2]/div')
            print(info.text)
        except Exception as e:
            logger.error(e)
            continue

        j = 1
        while True:
            logger.warning(f"页面提示\t{info.text}")
            logger.info(f"关于并发上限问题第{j}次尝试...")
            j += 1
            # 刷新
            sep = random.randint(0, 3)
            logger.info(f"等待{sep}秒后刷新")
            page.refresh()
            time.sleep(sep)

            try:
                info = page.ele('xpath://*[@id="app"]/div[1]/div/div/div/div[2]/div[2]/div')
                logger.info(f"页面提示\t{info.text}")
            except Exception as e:
                logger.error(e)
                logger.error("”提示元素“未找到")
                continue

            if info.text == "已达到用户并发数上限":
                break
            elif page.url == "http://10-17-27-11.newvpn.sdut.edu.cn:8118/#/login?redirect=%2F":
                logger.info("登录成功")
                return True, page

            print(page.url)
            logger.info("新的转机...")
            break

    return True, page

# TODO 配置
def start_browser(chromedriver_path):
    options = {
        'headless': False,  # 无头模式，不显示浏览器界面
        'disable_gpu': True,
        'no_sandbox': True,
        'disable_dev_shm_usage': True
    }
    try:
        page = ChromiumPage(chromedriver_path, options=options)
        page.timeout = 10
        return page
    except Exception as e:
        logger.error(f"ChromeDriver版本不匹配: {e}")
        logger.info("查看:")
        logger.info("https://googlechromelabs.github.io/chrome-for-testing/#stable")
        sys.exit(1)


def logout(page):
    print(page.cookies)
    page.cookies.clear()
    print(page.cookies)


if __name__ == '__main__':
    auth_sdut()
