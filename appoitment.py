import json
import random
import threading
import time

from DrissionPage._functions.keys import Keys
from DrissionPage.errors import ContextLostError

import CONSTRANTS
from Chrome import Chrome
from auth_sdut import deal_notice
import config_reader
import my_logger
from auth_sdut import auth_sdut

logger = my_logger.MYLogger().logger


def login():
    state, page = auth_sdut()
    if state == 1:
        logger.info("准备登录智慧体测系统...")
        # 获得账号密码
        opts = config_reader.load_config()
        username = opts.get('DEFAULT', 'username')
        password = opts.get('DEFAULT', 'password')
        # 判空
        if not username or not password:
            logger.error("账号或密码为空，请配置你的账号信息")
            return False

        # 登录
        input_element_u = page.ele('css:input.van-field__control[placeholder="学生为学号,教师为工号"]')
        input_element_u.clear()
        input_element_u.input(username)
        input_element_p = page.ele('css:input.van-field__control[type="password"]')
        input_element_p.clear()
        input_element_p.input(password)

        # 点击登录
        lgn_btn = page.ele('css:button[type="submit"]')
        lgn_btn.click(by_js=True)
    elif state == 2:
        deal_notice(page)
    return page


def appointment(page):
    appointment_page = page.ele('xpath://*[@id="app"]/div[1]/div[2]/div[2]/div[2]')
    appointment_page.click(by_js=True)
    from config_reader import load_config
    opts = load_config()
    policy = opts.get('DEFAULT', 'policy')
    # 室内
    if policy == '1':
        inner_ap_while(page)
    elif policy == '2':
        outer_ap_while(page)
    elif policy == '3':
        th1 = threading.Thread(target=inner_ap_while, args=(page,))
        th2 = threading.Thread(target=outer_ap_while, args=(Chrome().get_browser().new_tab(CONSTRANTS.INNER_URL),))
        th1.start()
        th2.start()
        th1.join()
        th2.join()
        print("线程已启动")
    elif policy == '4':
        while not inner_ap_dev(page):
            time.sleep(random.randint(1, 3))
    else:
        logger.error("未找到对应的策略")
        return False
    logger.info("预约结束,成功预约")


def outer_ap(page):
    logger.warning("进行室外预约..")

    page.get(CONSTRANTS.OUTER_URL)

    # 获得日期条目
    date_items = page.eles('css:#app > div.page > div:nth-child(3) > div.scrollBox > *')
    for date_item in date_items:
        div_element = date_item.ele('xpath:./*[1][self::div]')
        if div_element:
            logger.warning("当前日期\t%s", div_element.text)
        else:
            logger.error("当前日期\t未找到对应的div元素")

        date_item.click(by_js=True)

        time_periods = page.eles('css:#app > div.page > div:nth-child(3) > div:nth-child(2) > div > *')
        for time_period in time_periods:
            time_period.click(by_js=True)
            page.wait.ele_displayed('css:.quanbu-data.quanbu-data_tow')
            items = page.eles('css:.quanbu-data.quanbu-data_tow')
            for item in items:
                try:
                    group = item.child(index=1)
                    # 获取测试时间
                    time_span = group.child(index=1)
                    test_time = time_span.text.strip() if time_span else "未获取到测试时间"

                    # 获取测试地点
                    place_span = group.child(index=2)
                    test_place = place_span.text.strip() if place_span else "未获取到测试地点"

                    # 获取报名人数
                    enrollment_span = group.child(index=4)
                    enrollment_count = enrollment_span.text.strip() if enrollment_span else "未获取到报名人数"

                    logger.info("时间: %s, 地点: %s, 报名人数: %s", test_time, test_place, enrollment_count)

                    # 判断人数情况
                    is_full_enrollment(enrollment_count)
                    if is_full_enrollment(enrollment_count):
                        logger.debug("当前时间段已满")
                        continue

                    # 尝试点击预约按钮
                    reserve_button = item.child(index=2).child(index=1).child(index=1)
                    if reserve_button:
                        page.listen.start("/api/tzjc/testappointment/apply")
                        reserve_button.wait.clickable()
                        reserve_button.click(by_js=True)
                        logger.info("已尝试点击预约按钮,等待后端处理")
                        res = page.listen.wait()
                        logger.info("预约结果: %s", res.response.body)
                        if res.response.body['status'] == 1:
                            logger.info("预约成功")
                            return True
                    else:
                        logger.info("未找到预约按钮")
                except Exception as e:
                    logger.error("处理item时出错: %s", str(e))
    return False


def inner_ap(page):
    logger.warning("进行室内预约...")
    page.get(CONSTRANTS.INNER_URL)
    address_bar_js = f"window.location.href = '{CONSTRANTS.INNER_URL}';"
    page.run_js(address_bar_js)
    page.refresh()
    page.wait(1)
    # 获得日期条目
    date_items = page.eles('css:#app > div.page > div:nth-child(3) > div.scrollBox > *')
    for date_item in date_items:
        div_element = date_item.ele('xpath:./*[1][self::div]')
        if div_element:
            logger.warning("当前日期\t%s", div_element.text)
        else:
            logger.error("当前日期\t未找到对应的div元素")

        date_item.click(by_js=True)
        time.sleep(1)
        page.wait.eles_loaded('css:#app > div.page > div:nth-child(3) > div:nth-child(2) > div > *')
        time_periods = page.eles('css:#app > div.page > div:nth-child(3) > div:nth-child(2) > div > *')
        for time_period in time_periods:
            time_period.click(by_js=True)
            page.wait.ele_displayed('css:#app > div.page > div:nth-child(3) > div:nth-child(3)')
            items = page.eles('css:#app > div.page > div:nth-child(3) > div:nth-child(3)')
            for item in items:
                try:
                    group = item.child(index=1)
                    # 获取测试时间
                    time_span = group.child(index=1)
                    test_time = time_span.text.strip() if time_span else "未获取到测试时间"

                    # # 获取测试地点
                    # place_span = group.child(index=2)
                    # test_place = place_span.text.strip() if place_span else "未获取到测试地点"

                    # 获取报名人数
                    enrollment_span = group.child(index=3)
                    enrollment_count = enrollment_span.text.strip() if enrollment_span else "未获取到报名人数"

                    logger.info("时间: %s,  报名人数: %s", test_time, enrollment_count)

                    # 判断人数情况
                    if is_full_enrollment(enrollment_count):
                        logger.info("当前时间段已满")
                        continue

                    # 尝试点击预约按钮
                    reserve_button = item.child(index=2).child(index=1).child(index=1)
                    if reserve_button:
                        page.listen.start("/api/tzjc/testappointment/apply")
                        reserve_button.wait.clickable()
                        reserve_button.click(by_js=True)
                        logger.info("已尝试点击预约按钮,等待后端处理")
                        res = page.listen.wait()
                        logger.info("预约结果: %s", res.response.body)
                        if res.response.body['status'] == 1:
                            logger.info("预约成功")
                            return True
                    else:
                        logger.info("未找到预约按钮")
                except Exception as e:
                    logger.error("处理item时出错: %s", str(e))
    return False


def is_full_enrollment(enrollment_str):
    parts = enrollment_str.split(": ")[1].split("/")
    return int(parts[0]) >= int(parts[1])


def inner_ap_dev(page):
    try:
        logger.warning("进行室内预约...")
        page.get(CONSTRANTS.INNER_URL)
        address_bar_js = f"window.location.href = '{CONSTRANTS.INNER_URL}';"
        page.run_js(address_bar_js)
        # page.refresh()
        # page.wait(1)
        # 获得日期条目
        date_items = page.eles('css:#app > div.page > div:nth-child(3) > div.scrollBox > *')
        for date_item in date_items:
            div_element = date_item.ele('xpath:./*[1][self::div]')
            if div_element:
                logger.warning("当前日期\t%s", div_element.text)
            else:
                logger.error("当前日期\t未找到对应的div元素")

            date_item.click(by_js=True)
            time.sleep(1)
            page.wait.eles_loaded('css:#app > div.page > div:nth-child(3) > div:nth-child(2) > div > *')
            time_periods = page.eles('css:#app > div.page > div:nth-child(3) > div:nth-child(2) > div > *')
            for time_period in time_periods:
                page.listen.start(CONSTRANTS.AP_LIST)
                time_period.click(by_js=True)
                list = page.listen.wait()
                auth = list.request.headers['Authorization']
                check_and_book(list.response.body, page, auth)
    except ContextLostError as e:
        logger.error(f"上下文丢失: {str(e)}")
        return False
    return False

def outer_ap_dev(page):
    logger.warning("进行室外预约..")
    page.get(CONSTRANTS.OUTER_URL)
    address_bar_js = f"window.location.href = '{CONSTRANTS.OUTER_URL}';"
    page.run_js(address_bar_js)
    page.refresh()
    # page.wait(1)
    # 获得日期条目
    date_items = page.eles('css:#app > div.page > div:nth-child(3) > div.scrollBox > *')
    for date_item in date_items:
        div_element = date_item.ele('xpath:./*[1][self::div]')
        if div_element:
            logger.warning("当前日期\t%s", div_element.text)
        else:
            logger.error("当前日期\t未找到对应的div元素")

        date_item.click(by_js=True)

        time_periods = page.eles('css:#app > div.page > div:nth-child(3) > div:nth-child(2) > div > *')
        for time_period in time_periods:
            page.listen.start(CONSTRANTS.AP_LIST)
            time_period.click(by_js=True)
            list = page.listen.wait()
            auth = list.request.headers['Authorization']
            check_and_book(list.response.body, page, auth)
    return False

def send_ap(id, page, authorization):
    try:
        page.change_mode(mode='s')
        res = page.post(CONSTRANTS.AP_APPLY,
                        json={'appointmentId': [int(id)]},
                        headers={
                            'Authorization': authorization,
                            "content_type": "application/json",
                            "origin": "http://10-17-27-11.newvpn.sdut.edu.cn:8118",
                            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
                        },
                        allow_redirects=False)
        if res is None:
            return False, "请求失败", page
        if res.status_code != 200:
            return False, f"请求失败，状态码: {res.status_code}, 信息：{res.text}", page
    except Exception as e:
        logger.error(f"预约时出错: {str(e)}")
        return False, str(e), page
    finally:
        page.change_mode(mode='d', go=False)
    r = json.loads(res.text)
    if r["status"] != 1:
        return False, res.text, page
    return True, res.text, page


def check_and_book(json_data, page, auth):
    """
    检查JSON数据格式并根据条件判断预约情况并尝试预约
    :param json_data: 包含预约相关信息的JSON格式数据
    """
    try:
        # 解析JSON数据
        # 判断是否为字符串
        if isinstance(json_data, str) or json_data is None:
            logger.error("输入的JSON数据是字符串,或空:", json_data)
            return False
        data = json_data
        if not isinstance(data, dict) or "status" not in data or "message" not in data or "result" not in data:
            logger.error("输入的JSON数据格式不符合预期，缺少必要的键")
            return False

        status = data["status"]
        message = data["message"]
        result = data["result"]

        if not isinstance(result, list):
            logger.error("JSON数据中'result'字段不是列表类型，不符合预期格式")
            return False

        for index, item in enumerate(result):
            if not isinstance(item, dict) or "dateStart" not in item or "numMax" not in item or "numApply" not in item:
                logger.error(f"在'result'列表中的第 {index + 1} 个元素格式不符合预期，缺少必要的键")
                continue

            date_start = item["dateStart"]
            num_max = item["numMax"]
            num_apply = item["numApply"]

            # 判断是否可以预约，这里简单以 num_apply < num_max 为条件，你可根据实际规则调整
            if num_apply < num_max:
                try:
                    # 调用假设已经封装好的app函数进行预约，传入对应id（这里假设每个预约信息里有'id'字段）
                    stat, msg, page = send_ap(item["id"], page, auth)
                    if stat:
                        logger.info(f"成功预约 {date_start} 的时段，预约ID为 {item['id']}, {num_apply}/{num_max}, 返回信息: {msg}")
                        return True
                    else:
                        logger.error(f"预约 {date_start} 的时段（ID: {item['id']}）, {num_apply}/{num_max}失败: {msg}")
                except Exception as e:
                    logger.error(f"预约 {date_start} 的时段（ID: {item['id']}）, {num_apply}/{num_max}时出错: {str(e)}")
            else:
                logger.info(f"{date_start} 的时段已满，无法预约，预约ID为 {item['id']}, 返回信息: 未发请求, {num_apply}/{num_max}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析出错: {str(e)}")

def inner_ap_while(page):
    while not inner_ap_dev(page):
        time.sleep(random.randint(1, 3))

def outer_ap_while(page):
    while not outer_ap_dev(page):
        time.sleep(random.randint(1, 3))


