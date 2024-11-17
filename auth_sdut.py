import concurrent
import os
import random
import time
import sys
from DrissionPage import ChromiumPage
from DrissionPage import Chromium
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._pages.session_page import SessionPage

from Chrome import Chrome
from config_reader import load_config
import CONSTRANTS
import my_logger

logger = my_logger.MYLogger().logger


def auth_sdut():
    i = 1
    try:
        page = Chrome().get_browser().latest_tab
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
        if check_login_page(page):
            logger.info("当前在登录页")
            return 1, page
        if have_login(page):
            logger.info("登录成功,当前登录态")
            return 2, page
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
            time.sleep(random.randint(2, 3))
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
        logger.info("正在认证...")
        # 是否登录
        if have_login(page):
            logger.info("登录成功,当前登录态")
            return 2, page
        # 是否在登录页
        if check_login_page(page):
            logger.info("当前在登录页")
            return 1, page

        try:
            info = page.ele('xpath://*[@id="app"]/div[1]/div/div/div/div[2]/div[2]/div')
            if info:
                logger.warning(f"页面提示\t{info.text}")
        except Exception as e:
            logger.error("认证结果出现了没有预期的结果", e)
            continue
        # 刷新
        sep = random.randint(0, 3)
        logger.info(f"等待{sep}秒后刷新")
        time.sleep(sep)
    return True, page


def logout(page):
    print(page.cookies)
    page.cookies.clear()
    print(page.cookies)


def check_login_page(page):
    try:
        page.wait.doc_loaded()
        # 尝试获取特定的输入框元素
        input_element = page.ele('css:input.van-field__control[placeholder="学生为学号,教师为工号"]',
                                 timeout=0.5)
        if input_element:
            logger.info("找到了学生为学号,教师为工号的输入框，确认已在登录页。")
            return True
    except Exception as e:
        logger.info(f"未能找到特定输入框: {e}")
    logger.info("未能确认是否在登录页。")
    return False


def have_login(page):
    # 检查通知情况
    # msg = page.ele('css:button.van-button.van-button--default.van-button--large.van-dialog__confirm', time)
    # if msg:
    #     time.sleep(1)
    #     msg.click()
    #     return True
    sp_ele = page.ele(
        'css:#app > div:nth-child(1) > div.van-hairline--top-bottom.van-tabbar.van-tabbar--fixed > div.van-tabbar-item.van-tabbar-item--active > div.van-tabbar-item__text')
    if sp_ele not in [None, ''] and sp_ele.text == '首页':
        return True
    return False


def deal_notice(page):
    # page.listen.start(CONSTRANTS.NOTICE_URL)
    # page.refresh()
    # res = page.listen.wait()
    # notices = res.response.body
    # print(notices)
    # for notice in notices['result']['result']:
    #     logger.info(notice)
    # notices_ele = page.eles('xpath://*[@id="app"]/div[@class="announcement"]/div[@class="main"]/div/div/*')
    # for ele in notices_ele:
    #     notice = ele.click()
    #     page.back()
    pass


def get_sdp_user_token(bs):
    for coo in bs.cookies(all_info=True):
        if coo['domain'] == '.newvpn.sdut.edu.cn' and coo['name'] == 'sdp_user_token' \
                and coo['value'] not in ['', None]:
            # 判断是否过期
            if coo['expires'] == -1:
                # 是会话cookie，认为当前会话内有效，返回其值
                return coo['value']
            else:
                current_time = time.time()
                if current_time > coo['expires']:
                    # 已过期，返回None
                    return None
                else:
                    # 未过期，返回其值
                    return coo['value']
    return None